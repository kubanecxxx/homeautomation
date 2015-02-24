'''
@package docstring
@date Created on 30. 3. 2014

@author: kubanec
'''

##
# @defgroup dispatcher_package
# @brief   dynamic reloading of user modules, data frames distribution between
# hardware and the user modules
# @{

##
# @defgroup dispatcher
# @brief reloading of user modules, intercommunication of those modules between
# hardware
# @{

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
import inspect, os
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/.." # script directory


##
# @brief Dynamic reloading user modules and message distribution between
# hardware and those modules 
#
#    Modules are added/reloaded automatically and on the fly (no restart needed)
#
#    Only one instance is used in whole application. 
class dispatcher:
    ##
    # @brief message codes to user readable string conversion table
    _table = {serialHardware.Hardware.NEW_DATA : "NEW_DATA", 
             serialHardware.Hardware.ERROR: "ERROR",
             serialHardware.Hardware.TX_FAILED: "TX_FAILED",
             serialHardware.Hardware.TX_FINISHED: "TX_FINISHED"}

    ## 
    # @brief Initialize instance variables, create dedicated thread and
    # create hardware class instance
    def __init__(self):
        ## @brief hardware instance
        self._hw = serialHardware.Hardware(self._handle_events) #hardware connector        
        ## @brief dedicated thread
        self._thread = Thread(target=self._loop,name="dispatcher")
        self._thread.setDaemon(True)
        ## @brief instance logger
        self._log = logging.getLogger("root.dispatcher")
        self._lock = Lock()
        ## @brief list of user modules
        self._objects = {}
        ## @brief command table
        self._command_table = commandTable.commands
        self._log_apps = logging.getLogger("root.apps")
        pass
    
    ##
    # @brief open hardware and start dedicated thread
    def start(self):
        self._hw.open("/dev/ttyUSB0")
        self._thread.start()
        pass
    
    ##
    # @brief format serial data to command and payload
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
    
    ##
    # @brief receive callbacks from @ref hardware class and distribute
    # data to the dynamically imported user modules
    #
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
            if (arg[2] == self.command_table().STARTUP):
                self._log.warning("pipe %d (%s) firmware just started-up" % (pipe,self.command_table().stations[pipe]))
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
                f._log.exception("Raised exception")
        self._lock.release()
        
    
    ##
    # @brief  thread code checks for changes in user modules and @ref commandtable
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
            
            
    ##
    # @brief refresh list of user modules in package @ref aplications
    # search for new modules and dynamically import them and modified modules
    # are dynamically reimported
    def _get_objects(self, objects):
        # @type objects: {}
        filename = os.path.abspath(path + "/aplications")
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
    
    ##
    #   @brief Used by user modules to send arbitrary data to the wireless modules
    #   @param pipe [int]  Logical address of wireless module 
    #    @param command [int]  Arbitrary command from @ref command_table
    #    @param data [int/character array] User data array of bytes or integer which is automatically
    #    converted to the byte of array
    #    @param integerLength [int]  If data is integer it will be converted to specified 
    #    number of bytes
    def send_packet(self, pipe, command, data = None, integerLength = None):
        # @type pipe: int 
        # @type command: int
        # @type data: array.array("B") 
        payload = array.array("c")
        
        if data is not None:    
            if isinstance(data,array.array):
                payload.fromstring(data.tostring())
            if isinstance(data, int):
                t = data                
                if type(integerLength) is int:
                    while integerLength > 0:
                        payload.append(chr(t & 0xff))
                        t >>= 8
                        integerLength -= 1
                        
                else:    
                    while t:
                        payload.append(chr(t & 0xff))
                        t >>= 8
            
        command |= self._command_table.WRITE_FLAG    
        payload.insert(0,chr((command >> 8) & 0xff))
        payload.insert(0,chr(command & 0xff))
        
        self._log.info("send ack payload pipe %d, command %d, load %s",pipe,command,str(data))
        self._log.info("send ack payload raw: %s" ,str(payload))
        self._hw.put_ack_payload(pipe, payload)
         
        pass
    
    ##
    # @brief returns command table which is automatically reloaded after modification
    #    on the fly
    @property
    def command_table(self):
        return self._command_table
    
    #@}
    
#@}