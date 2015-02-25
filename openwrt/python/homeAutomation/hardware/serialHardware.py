##
# @defgroup hardware
# @brief Communicaion with hardware with (virtual) serial port 
# @{

import serial
from crc8 import crc8
import array
from threading import Thread, Lock 
from events import events
import Queue
import pickle
import time
import logging
from threading import Timer

##
# @defgroup serial_commands
# @brief serial frame description <b>the most crucial think - you don't need to
# use this directly there is an API in @ref Hardware</b>
#  
# the 7th bit meaning:
#    + 1 receive from USB/wireless adaptor
#    + 0 sending to the adaptor
# @details this table is basically the same in the USB/wireless adaptor
# 
# @note this module is basically the same in the USB/wireless adaptor MCU
# firmware but the firmware is written in C so enum is used instead
# 
# Data structure of the serial frame (both directions are the same):
# <table>
# <tr>
# <td> 1byte </td> <td> 1byte </td> <td> 1byte </td>
# <td> according to the payload_size </td><td> 1byte </td>
# </tr>
# <tr>
# <td>PREAMBLE 0x44 </td><td> @ref serial_commands code </td>
# <td>payload size </td><td>payload </td><td> CRC</td>
# </tr>
# </table>
#
# @{

## @brief preamble is always on the start of any serial frame
PREAMBLE = 0x44

## @brief send data to pipe
#
# NRF24L01 module can accept maximum data packet size 32bytes.
# structure of serial payload is:
#   + 1st payload byte is pipe - logical address of wireless slave module
#   + 2nd - 33th wireless data itself
#
# so serial payload size can be at max 33 bytes, payload can be shorter. There
# is no need to send all 32 bytes over air for nothing
RF_SEND_PIPE = 0x00
## @brief force hardware to discard transmit buffer
# no payload 
RF_FLUSH_TX = 0x01
## @brief force hardware to discard receive buffer
# no payload 
RF_FLUSH_RX = 0x02
## @brief clear watchdog in hardware
# no payload 
RESET_WATCHDOG = 0x03
## @brief say to hardware to disable/enable serial data output 
# 1 byte payload:
#   + 0 disable output
#   + 1 enable output
DISABLE_NEW_DATA_OUTPUT = 0x04

## @brief new wireless data from hardware
# 
# same behaviour like @ref RF_SEND_PIPE
RF_NEW_DATA = 0x80
## @brief hardware has empty transmitting buffer
# 
# one payload byte - pipe number module which data was sent to
RF_TX_END = 0x81
## @brief crc validation in hardware failed
#
# it is not used by application just log message is created
#
# @todo how does it work? who knows
CRC_FAILED = 0x82
## @brief this application sent invalid data to hardware and the hardware is 
# angry
#
# it is not used by this application
#
# @todo how does it work? does anybody know?
INVALID_COMMAND = 0x83
## @brief sent by hardware on startup
#
# no payload
HARDWARE_STARTUP = 0x84

##
# @}

class Hardware:
    
    ##
    # @defgroup dispatcher_codes 
    # @brief these codes are passed to the @ref dispatcher through callbacks
    # @{
    
    ## @brief new data arrived
    NEW_DATA = 0
    ## @brief data transmition finished correctly
    TX_FINISHED = 1
    ## @brief data transmition failed
    TX_FAILED = 2
    ## @other errors (CRC failed)
    ERROR = 3
    ##
    # @}
    
    ##
    # @brief create instance of hardware communication class
    # @param all_cb central callback called when one of other callbacks is going to be called
    # @param new_data_cb new data arrived from wireless slave module callback
    # @param ack_packet_finished transmitting to wireless slave successfully finished
    # @param error_cb error occured callback
    # @param client_unrecheable wireless slave cannot be reached - transmittion timeout
    def __init__(self, all_cb=None, new_data_cb=None, ack_packet_finished_cb=None, error_cb=None, client_unreachable=None):
        self._com = ""
        self._serial = serial.Serial
        self._idx = 0
        self._buffer = []
        self._crc = crc8()
        ## @brief comport reading thread
        self._thread = Thread(target=self._loop, name="comport")
        self._thread.setDaemon(True)
        self._run = True
        self._newdata_cb = new_data_cb
        self._ack_packet_finished_cb = ack_packet_finished_cb
        self._client_unreachable = client_unreachable
        self._error_cb = error_cb
        self._master_cb = all_cb
        self._lock = Lock()
        ## @brief wireless transmition packet queue processing thread
        self._send_thread = Thread(target=self._sending_loop2, name="ack payload sender")
        self._send_thread.setDaemon(True)
        self._send_queue = Queue.Queue()
        self._packet_inside = False        
        self._buffer = []
        self._log = logging.getLogger("root.serialHardware")
        self._tx_finished_lock = Lock()
        self._loop_idx = 0
        self._loop_reciver_timeout_lock = Lock()
        
    ##
    # @brief open serial port 
    # @param path_serial full path to the comport (e.g. /dev/ttyS0)
    # @todo baudrate from configfile
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

    ##
    # @brief close comport and terminate threads
    def close(self):
        self._run = False
        self._serial.close()
        pass

    ##
    # @brief force USB/wireless adapter hardware to discard transmit buffer
    def flush_tx(self):
        self._put_command_packet(RF_FLUSH_TX)
        pass

    ##
    # @brief force USB/wireless adapter hardware to discard receive buffer
    def flush_rx(self):
        self._put_command_packet(RF_FLUSH_RX)
        pass

    ##
    # @brief reset USB/wireless adapater watchdog timer
    def reset_watchdog(self):
        self._put_command_packet(RESET_WATCHDOG)
        pass

    ##
    # @brief enable or disable USB/wireless adapter serial output
    # @param enable 
    #    + 1 enable serial output
    #    + 0 disable serial output
    def enable_new_data_output(self, enable):
        a = array.array("c", chr(enable))
        self._put_command_packet(DISABLE_NEW_DATA_OUTPUT, a)
        pass

    ##
    # @brief high level api - send data to the wireless slave
    # @param pipe [int] logical address of slave
    # @param payload [array.array("c")] data load
    def put_ack_payload(self, pipe, payload):
        # @type payload: array.array("c")
        # @type pipe: int
        p = payload[:]
        t = []
        t.append(pipe)
        t.append(p)
        self._send_queue.put(t)
        # self._put_command_packet(RF_SEND_PIPE, payload)

    ##
    # @brief write serial command packet to the USB/wireless adapter
    # encode packet serial data; adds preamble and crc
    # @param command [@ref serial_commands ]
    # @param payload [array.array("c")] arbitrary data 
    # @todo document serial frame
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

    ##
    # @brief receiving thread loop 
    # if exception occurs it will schedule appliation exit
    def _loop(self):
        try:
            self.__loop()
        except:
            events.event.register_exit()
        
    ##
    # @brief wireless frame sending thread loop 
    # if exception occurs it will schedule appliation exit
    def _sending_loop2(self):
        try:
            self.__sending_loop2()
        except:
            events.event.register_exit()

    ##
    # @brief shit could happen - if longer time no data arrives from 
    # USB/wireless adaptor serial frame decoding state machine will be
    # reset to zero
    def _receiver_timeout(self):
        self._loop_reciver_timeout_lock.acquire()
        self._loop_idx = 0
        self._loop_reciver_timeout_lock.release()
        self._log.warn("receiving timeout - byte index reset to 0")
        pass

    ##
    # @brief recieving thread code
    #
    # takes bytes from serial port decoding serial frames do crc validation 
    # and if the validation passes, frame processing function is called
    def __loop(self):
        command = 0 
        size = 0
        payload = array.array("c")
        self._loop_idx = 0
        crc = 0

        while True:
            try:
                char = self._serial.read(1)
            except:
                self._log.exception("serial exception - probably device disconnected")
                events.event.register_exit()
                
            char = int(char.encode("hex"), 16)
            self._loop_reciver_timeout_lock.acquire()

            if self._loop_idx == 0:
                tmr = Timer(0.5,self._receiver_timeout)
                tmr.start()    
                if char != PREAMBLE:
                    self._loop_idx = 0
                    crc = 0
                    del(payload[:])

            elif self._loop_idx == 1:
                command = char

            elif self._loop_idx == 2:
                size = char

            elif self._loop_idx >= 3:
                payload.append(chr(char))

            if self._loop_idx != 0:
                crc = self._crc.crcByte(crc, char)
            if self._loop_idx - 3 == size:
                # i = 1
                payload.pop()
                # do stuff with packet
                if crc is 0:
                    self._do_packet(command, payload)
                else:
                    self._log.warning("recieved serial packet crc failed")
                
                # reinit state machine
                crc = 0
                tmr.cancel()
                self._loop_idx = -1
                del(payload[:])

            self._loop_idx += 1
            self._loop_reciver_timeout_lock.release()
        pass
    
    ##
    # @brief called when valid serial frame is received from USB/wireless adaptor
    #
    # process received frame and send callback to the master dispatcher
    # 
    # @param command [@ref serial_command]
    # @param payload [array.array("c")]
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
        
        # register particular callback
        if cb is not None:
            events.event.register_event(cb, args)
        
        # register master callback if exits
        if self._master_cb is not None and t is not None:
            events.event.register_event(self._master_cb, t)
            
    ##
    # @brief testing function - not used
    # @deprecated
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
    
    ##
    # @brief testing function - not used
    # @deprecated
    def pak(self):
        time.sleep(30)
        payload = array.array("c")
        payload.append(chr(7))
        payload.append(chr(0))
        payload.append(chr(1))
        payload.append(chr(2))
        self.put_ack_payload(4, payload)

    ##
    # @brief wirless frames sending thread code; holds wireless frames in buffer
    # because hardware has buffer only for 3 packets
    #
    # sends packet one by one if there is a free space the hardware queue
    # after certain timeout the whole buffer of hardware is discarded
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
                 
    ##
    # @brief old version of wireless packet sending thread code
    # @deperacated
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
            
    ##
    # @brief send serial frame to the USB/wireless adaptor to send wireless frame
    # to wireless slave                       
    def _put_ack_payload(self, p):
        a = p[1]
        a = a[:]
        a.insert(0, chr(p[0]))
        self._put_command_packet(RF_SEND_PIPE, a)
        
        
#@}
