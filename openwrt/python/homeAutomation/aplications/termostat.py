'''
Created on 30. 3. 2014

@author: kubanec
'''

from hardware.serialHardware import Hardware
from aplications.baseClass import baseClass
from dispatcher.commandTable import commands
from dispatcher.dispatcher import dispatcher
import logging
import array
import time

class app(baseClass):
    def __init__(self,name):
        baseClass.__init__(self,name)
        
        #individual basic setup
        self.vmt[Hardware.NEW_DATA] = self.new_data
        self.vmt[Hardware.TX_FINISHED] = self.cosi
        #self.vmt[Hardware.TX_FAILED] = self.err
        self._pipe_list = [0, 1]

        self.i = 0
        #logging.getLogger("root.dispatcher").setLevel(logging.WARN)
   
    def new_data(self,args):
        #@type dispatcher: dispatcher
        #@type pipe: int
        #@type command: int
        #@type payload: array.array("B")
        dispatcher,pipe,command,payload = args

        #print pipe
        #print command
        #print payload.tolist()
        c = 7

        print payload;          
        if (self.i % 4) == 0:            
            dispatcher.send_packet(0, c )
            #dispatcher.send_packet(1, c )
            
        self.i += 1
        
        pass 
    
    def cosi(self,args):
        
        pass
    
    def err(self,args):
        print args
        