__author__ = 'kubanec'

import serial
from crc8 import crc8
import array
from threading import Thread, Lock 
from events import events
import Queue
import pickle
import time
import logging

PREAMBLE = 0x44

# commands
RF_SEND_PIPE = 0x00
RF_FLUSH_TX = 0x01
RF_FLUSH_RX = 0x02
RESET_WATCHDOG = 0x03
DISABLE_NEW_DATA_OUTPUT = 0x04

RF_NEW_DATA = 0x80
RF_TX_END = 0x81
CRC_FAILED = 0x82
INVALID_COMMAND = 0x83
HARDWARE_STARTUP = 0x84

class Hardware:
    
    NEW_DATA = 0
    TX_FINISHED = 1
    TX_FAILED = 2
    ERROR = 3
    
    def __init__(self, all_cb=None, new_data_cb=None, ack_packet_finished_cb=None, error_cb=None, client_unreachable=None):
        self._com = ""
        self._serial = serial.Serial
        self._idx = 0
        self._buffer = []
        self._crc = crc8()
        self._thread = Thread(target=self._loop, name="comport")
        self._thread.setDaemon(True)
        self._run = True
        self._newdata_cb = new_data_cb
        self._ack_packet_finished_cb = ack_packet_finished_cb
        self._client_unreachable = client_unreachable
        self._error_cb = error_cb
        self._master_cb = all_cb
        self._lock = Lock()
        self._send_thread = Thread(target=self._sending_loop2, name="ack payload sender")
        self._send_thread.setDaemon(True)
        self._send_queue = Queue.Queue()
        self._packet_inside = False        
        self._buffer = []
        self._log = logging.getLogger("root.serialHardware")
        self._tx_finished_lock = Lock()
        

    def open(self, path_serial):
        self._log.info("opening com port...")
        self._com = path_serial
        self._serial = serial.Serial(path_serial, 9600, timeout=None)
        self.enable_new_data_output(1)
        self.flush_tx()
        self._log.info("comport openened")
        
        # init reading thread
        self._thread.start()
        self._send_thread.start()

        #self.volej()

    def close(self):
        self._run = False
        self._serial.close()
        pass

    def flush_tx(self):
        self._put_command_packet(RF_FLUSH_TX)
        pass

    def flush_rx(self):
        self._put_command_packet(RF_FLUSH_RX)
        pass

    def reset_watchdog(self):
        self._put_command_packet(RESET_WATCHDOG)
        pass

    def enable_new_data_output(self, enable):
        a = array.array("c", chr(enable))
        self._put_command_packet(DISABLE_NEW_DATA_OUTPUT, a)
        pass

    # high level api
    def put_ack_payload(self, pipe, payload):
        # @type payload: array.array("c")
        # @type pipe: int
        p = payload[:]
        t = []
        t.append(pipe)
        t.append(p)
        self._send_queue.put(t)
        # self._put_command_packet(RF_SEND_PIPE, payload)

    def _put_command_packet(self, command, payload=None):
        # @type payload: array.array
        # generate crc
        crc = 0
        size = 0
        if payload is not None:
            size = len(payload)
        
        self._log.info("command written to hardware: %d; payload:" + str(payload) , command)
        
        crc = self._crc.crcByte(crc, command)
        crc = self._crc.crcByte(crc, size)

        data = chr(PREAMBLE)
        data += chr(command)
        data += chr(size)
        if payload is not None:
            for c in payload:
                crc = self._crc.crcByte(crc, ord(c))
            data += payload.tostring()
        data += chr(crc)

        self._lock.acquire()
        self._serial.write(data)
        self._log.debug("data written to hardware (hex) %s", data.encode("hex"))
        self._lock.release()

    def _loop(self):
        try:
            self.__loop()
        except:
            events.event.register_exit()
        
    def _sending_loop2(self):
        try:
            self.__sending_loop2()
        except:
            events.event.register_exit()

    def __loop(self):
        command = 0 
        size = 0
        payload = array.array("c")
        idx = 0
        crc = 0

        while True:
            try:
                char = self._serial.read(1)
            except:
                self._log.exception("serial exception - probably device disconnected")
                events.event.register_exit()
                
            char = int(char.encode("hex"), 16)

            if idx == 0:
                if char != PREAMBLE:
                    idx = 0
                    crc = 0
                    del(payload[:])

            elif idx == 1:
                command = char

            elif idx == 2:
                size = char

            elif idx >= 3:
                payload.append(chr(char))

            if idx != 0:
                crc = self._crc.crcByte(crc, char)
            if idx - 3 == size:
                # i = 1
                payload.pop()
                # do stuff with packet
                if crc is 0:
                    self._do_packet(command, payload)
                else:
                    self._log.warning("recieved serial packet crc failed")
                
                # reinit state machine
                crc = 0
                idx = -1
                del(payload[:])

            idx += 1
        pass
    
    def _do_packet(self, command, payload):
        # @type command: int
        # @type payload: array
        
        cb = None
        args = None
        t = None
        if command == RF_NEW_DATA:
            cb = self._newdata_cb
            pipe = payload.pop(0)
            args = (ord(pipe), payload)
            self._log.info("new data arrived from pipe %d : %s", ord(pipe), payload)
            t = (self.NEW_DATA, args)
            #restart watchdog timer
            self.reset_watchdog()
            
        elif command == RF_TX_END:
            if len(payload):
                cb = self._ack_packet_finished_cb
                args = ord(payload[0])
                self._log.info("packet delivered to pipe %d", args)
                t = (self.TX_FINISHED, args)

                self._tx_finished_lock.acquire()
                # vyhodit to z bufferu pryc
                mazat = None
                for p in self._buffer:
                    pipe = p[0]
                    if pipe == args:
                        mazat = p 
                        break
                    
                if mazat is not None:
                    self._buffer.remove(p)
                self._tx_finished_lock.release()
                
        elif command == HARDWARE_STARTUP:
            self._log.error("Hardware firmware just started-up")

        else:
            cb = self._error_cb
            args = command
            self._log.warning("master radio problem %d", args)
            t = (self.ERROR, args)
            pass
        
        if cb is not None:
            events.event.register_event(cb, args)
            
        if self._master_cb is not None and t is not None:
            events.event.register_event(self._master_cb, t)
            
    def volej(self):
        payload = array.array("c")
        payload.append(chr(7))
        payload.append(chr(0))
        payload.append(chr(1))
        payload.append(chr(2))
        self.put_ack_payload(1, payload)
        self.put_ack_payload(2, payload)
        self.put_ack_payload(3, payload)
        self.put_ack_payload(4, payload)
        self.put_ack_payload(5, payload)
        
        ja = Thread(target=self.pak)
        ja.start()
        #logging.getLogger("root.serialHardware").setLevel(logging.INFO)
        pass        
    
    def pak(self):
        time.sleep(30)
        payload = array.array("c")
        payload.append(chr(7))
        payload.append(chr(0))
        payload.append(chr(1))
        payload.append(chr(2))
        self.put_ack_payload(4, payload)

    def __sending_loop2(self):
        add = 0
        while self._run:
            self._tx_finished_lock.acquire()
            if not self._send_queue.empty():
                if len(self._buffer) < 3:
                    p = self._send_queue.get()
                    self._put_ack_payload(p)
                    self._buffer.append(p)
                    # add send time to packet structure
                    if len(p) < 3:
                        p.append(time.time())
                    
                    # pokud uz ve fronte neco a hned by se to vymazalo
                    # tak to zresetujeme vsude
                    if add > 15:
                        self._log.info("timeout has been reset")
                        for ble in self._buffer:
                            ble[2] = time.time()
                
            # pocitat timeout u jednotlivech paketu
            add = 0
            tim = time.time()
            for p in self._buffer:
                timeout = tim - p[2]
                # pokud bude soucet vsech timeout vetsi nez 
                # tak vyhodit vsechno - fuzzy logic
                add += timeout

            # pokud je soucet vsech timeoutu vetsi nez
            # tak vymaze frontu a buffer   
            # a uvedomi ostatni ze maji smulu
            if add > 25:
                self._log.warning("ack payload queue has been flushed due to timeout")
                self.flush_tx()
                
                for p in self._buffer:
                    if self._client_unreachable is not None:
                        events.event.register_event(self._client_unreachable,p )
                    if self._master_cb is not None:
                        t = (self.TX_FAILED, p)
                        events.event.register_event(self._master_cb, t)
                    self._log.warning("packet cannot be delivered " + str(p))                    

                self._buffer = []
                
            self._tx_finished_lock.release()
            time.sleep(1)
                 

    def _sending_loop(self):
        tim = 0
        last_packet = None
        while self._run:
            if self._packet_inside is False:
                p = self._send_queue.get()
                self._put_ack_payload(p)
                last_packet = p
                self._packet_inside = True
                tim = time.time()
            elif time.time() - tim > 2:
                if self._send_queue.empty() is False: 
                    p = self._send_queue.get(0.1)
                    self.flush_tx()
                    self._put_ack_payload(p)

                    if len(last_packet) == 3:
                        if last_packet[2] < 10:
                            self._send_queue.put(last_packet)
                    elif len(last_packet) == 2:
                        self._send_queue.put(last_packet)
                            
                    last_packet = p
                    tim = time.time()
                if last_packet is not None:    
                    if len(last_packet) == 2:
                        last_packet.append(0)
                    last_packet[2] += 1
                    if last_packet[2] >= 10:
                        self.flush_tx()
                        self._packet_inside = False
                        if self._client_unreachable is not None:
                            events.event.register_event(self._client_unreachable, last_packet)
                        if self._master_cb is not None:
                            t = (self.TX_FAILED, last_packet)
                            events.event.register_event(self._master_cb, t)
                        self._log.warning("packet cannot be delivered " + str(last_packet))                    
                        last_packet = None
                    
            time.sleep(0.1)
            
                        
    def _put_ack_payload(self, p):
        a = p[1]
        a = a[:]
        a.insert(0, chr(p[0]))
        self._put_command_packet(RF_SEND_PIPE, a)