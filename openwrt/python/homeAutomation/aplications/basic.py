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

class app(baseClass):
    def __init__(self,name):
        baseClass.__init__(self,name,False)
        
        self.vmt[Hardware.NEW_DATA] = self.new_data
        self._pipe_list = [8]
        
        pass
   
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
        print pipe
        
        pass 