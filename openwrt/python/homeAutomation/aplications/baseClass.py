'''
Created on 30. 3. 2014

@author: kubanec
'''

from hardware.serialHardware import Hardware
import logging

class baseClass:
    def __init__(self, name):
        # args in tuple
        self._vmt = {
                     Hardware.NEW_DATA : None,  # (dispatcher_instance, pipe, application_command, data)
                     Hardware.ERROR : None,  # (dispatcher_instance, error_code)
                     Hardware.TX_FAILED : None,  # (dispatcher_instance, pipe, application_command, data)
                     Hardware.TX_FINISHED : None  # (dispatcher_instance, pipe)
                     }
        self._name = name
        self._pipe_list = []
        self._log = logging.getLogger("root.apps." + name)
        self._log.info("Instance created: %s", name)

    @property
    def vmt(self):
        return self._vmt
    
    @property
    def pipe_list(self):
        return self._pipe_list
    
        
