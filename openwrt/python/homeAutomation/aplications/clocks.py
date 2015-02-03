'''
Created on 30. 3. 2014

@author: kubanec
'''

from hardware.serialHardware import Hardware
from aplications.baseClass import baseClass, log_to_db,print_pts
from dispatcher.commandTable import commands
from dispatcher.dispatcher import dispatcher
import logging
import array
import time
import MySQLdb as mdb
from dispatcher import commandTable



class app(baseClass):
    def __init__(self,name):
        baseClass.__init__(self,name,False)
        
        #individual basic setup
        self.vmt[Hardware.NEW_DATA] = self.new_data
        self.vmt[Hardware.TX_FINISHED] = self.cosi
        #self.vmt[Hardware.TX_FAILED] = self.err
        self._pipe_list = [2]

        self.i = 0
        self._idle_count = 0
        self._log.debug("startup joudo")
        #logging.getLogger("root.dispatcher").setLevel(logging.ERROR)        
                
        #logging.getLogger("root.serialHardware").setLevel(logging.ERROR)    
        FORMAT = '%(asctime)s  [%(name)s]:[%(levelname)s] - %(message)s'
        formater= logging.Formatter(FORMAT)

        self._log.handlers = []
        self._log.setLevel(logging.NOTSET)
        
        #return
                
        
        
    def _idle_data(self,send,table,pipe,command,load): 
        self._log.debug("idle from pipe %d" % pipe)
        
        if self._idle_count > 20:
            self._idle_count = 0 
            temp = 3600 * time.localtime().tm_isdst
            t = int(time.time() ) + temp 
            send(pipe,table.TIME_SINCE_EPOCH,t,4)
            self._log.info("time sent to pipe %d" % pipe)
            
        self._idle_count += 1
        return
    
    def _startup(self,send,table,pipe,command,load):
        t = int(time.time())
        send(pipe,table.TIME_SINCE_EPOCH,t,4)
    
    def new_data(self,args):
        dispatcher = args[0]
        table = dispatcher.command_table()
        self._command_table[table.IDLE] = self._idle_data
        self._command_table[table.STARTUP] = self._startup
#        logging.getLogger("root").setLevel(logging.INFO)
        self._command_handler(args)
        

             
    def cosi(self,args):
        self._log.info(str(args))
        
        pass
    
    def err(self,args):
        print args

        
