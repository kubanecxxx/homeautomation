'''
Created on 30. 3. 2014

@author: kubanec
'''

from hardware import serialHardware
from threading import Thread,Lock
import time
import commandTable
from aplications import baseClass
import imp 
import os
import logging
import array
import events

class dispatcher:
    def __init__(self):
        self._hw = serialHardware.Hardware(self._handle_events)
        self._thread = Thread(target=self._loop,name="dispatcher")
        self._thread.setDaemon(True)
        self._log = logging.getLogger("root.dispatcher")
        self._lock = Lock()
        self._objects = {}
        self._command_table = commandTable.commands
        self._log_apps = logging.getLogger("root.apps")

        pass
    
    def start(self):
        self._hw.open("/dev/ttyUSB0")
        self._thread.start()
        pass
    
    _table = {serialHardware.Hardware.NEW_DATA : "NEW_DATA", 
             serialHardware.Hardware.ERROR: "ERROR",
             serialHardware.Hardware.TX_FAILED: "TX_FAILED",
             serialHardware.Hardware.TX_FINISHED: "TX_FINISHED"}
    
    def _format_serial_data(self, args):
        pipe = args[0]
        data = args[1]
        if len(data) < 2:
            self._log.error("Invalid tx failed packet - too short payload")
            return
        command = ord(data[0]) | ord(data[1]) << 8
        data = data[2:len(data)]
        pole = array.array("B")
        pole.fromstring(data.tostring())
        t = (self, pipe, command ,pole)
        return t
    
    def _handle_events(self, args):
        code = args[0]
        args = args[1]
        
        # tuple with self and data needed by callbacks
        arg = None
        pipe = -1
        if code == self._hw.NEW_DATA:
            arg = self._format_serial_data(args)
            pipe = arg[1]
            self._log.debug("new packet pipe %d; command %d; load " + str(arg[3].tolist()),pipe,arg[2])
            pass
        elif code == self._hw.TX_FINISHED:
            #pipe number
            arg = (self,args)
            pipe = args
            self._log.debug("Packet delivered to pipe %d", pipe)
            pass
        elif code == self._hw.TX_FAILED:
            arg = self._format_serial_data(args)
            pipe = arg[1]
            self._log.warning("packet delivery failed %d; command %d; load " + str(arg[3].tolist()),pipe,arg[2])
            pass
        elif code == self._hw.ERROR:
            #error code
            arg = (self, args)
            self._log.warning("Error from hardware " + str(args))
            pass
        else:
            self._log.warning("_handle_events with invalid serialHardware code")
            return

        exp = self._table[code]
        
        self._lock.acquire()
        for a in self._objects.values():
            f = a[0]
            lst = f.pipe_list
            if not pipe in lst and not code == self._hw.ERROR:
                continue
            
            vmt = f.vmt
            cb = vmt[code]
            # @type lst: []

            try:
                if cb is not None:
                    cb(arg)
            except:
                self._log.exception("Application module \"%s\" raised exception in \"%s\" handler", f._name, exp)
        self._lock.release()
        
    
    def _loop(self):
        while True:    
            try:
                self._lock.acquire()
                self._objects = self._get_objects(self._objects)
                try:
                    reload(commandTable)
                    t = commandTable.commands.REFRESH_PERIOD
                except:
                    self._log.exception("Error in reloading command table")
                self._command_table = commandTable.commands
                self._lock.release()
                time.sleep(t)
            except:
                events.events.event.register_exit()
            
            
    def _get_objects(self, objects):
        # @type objects: {}
        filename = os.path.abspath("aplications")
        a = os.listdir(filename)
        a.remove("baseClass.py")
        a.remove("__init__.py")
        lst =[]
        b = ""
        for b in a:
            if not b.endswith(".py"):
                lst.append(b)
             
        for b in lst:
            a.remove(b)
       
        for b in a:
            name = filename + "/" +b
            scrname = b.rstrip(".py")
            mtime = os.path.getmtime(name)
            jo = False
            if scrname in objects:
                t = objects[scrname]
                t = t[1]
                if mtime == t:
                    continue
            else:
                jo = True
                self._log.info("new module \"%s\" was added", scrname)
                
            try:
                c = imp.load_source("modul", name)
                c = c.app(scrname)
                tup = (c, mtime)
                objects[scrname] = tup
            except:
                self._log.exception("module \"%s\" raised exception during import",scrname)
            if jo is False:
                self._log.info("module \"%s\" was changed", scrname)

            
        return objects  
                
    def send_packet(self, pipe, command, data = None):
        # @type pipe: int 
        # @type command: int
        # @type data: array.array("B") 
        payload = array.array("c")
        
        if data is not None:
            payload.fromstring(data.tostring())
            
        payload.insert(0,chr((command >> 8) & 0xff))
        payload.insert(0,chr(command & 0xff))
        
        self._hw.put_ack_payload(pipe, payload)
         
        pass
    
    @property
    def command_table(self):
        return self._command_table