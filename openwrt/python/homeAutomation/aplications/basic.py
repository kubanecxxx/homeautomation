## 
# @defgroup User_modules
# @{

from hardware.serialHardware import Hardware
from aplications.baseClass import baseClass
from dispatcher.commandTable import commands
from dispatcher.dispatcher import dispatcher
import logging
import array

##
# @brief basic user module class used only for testing
class app(baseClass):
    def __init__(self,name):
        baseClass.__init__(self,name,False)
        
        self._pipe_list = [0]
        print "startup"
        pass
   
    ## 
    # @base_virtual
    def virtual_new_data(self, dispatcher, pipe, command, payload):
        pass

   
    ## 
    # @base_virtual
    def virtual_tx_finished(self, dispatcher, pipe):
        print "test"
    
    ## 
    # @base_virtual    
    def virtual_tx_failed(self, dispatcher, pipe, command, data):
        pass

    ## 
    # @base_virtual
    def virtual_error(self, dispatcher, error_code):
        pass
        
##  @}
