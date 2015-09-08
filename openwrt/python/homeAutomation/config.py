import ConfigParser
import collections
import os
import sys
import logging

## @brief global configuration dictionary
config_dict = {}
## @brief global configuration data as a named tuple
config_named_tuple = None

##
# @brief read configuration data from configuration file
class application_config():
    def __init__(self, filename):
        p = ConfigParser.RawConfigParser()
        p.read([filename])
        #config_dict["usb"] = p.get("serial", "usb")
        config_dict["baudrate"] = p.getint("serial","baudrate")
        config_dict["db_name"]  = p.get("database","name")
        config_dict["db_password"]  = p.get("database","password")
        config_dict["db_host"]  = p.get("database","host")
        config_dict["db_database"] = p.get("database","database_name")
        config_dict["logging_control_port"] = p.getint("logging","control_port")
        
        
        #automatically find out the number of com port
        port = None
        for a in range(0,10):
            st = "/dev/ttyUSB%d" % a
            if os.path.exists(st):
                port = st
                break
        
        if not port:
            logging.getLogger("root").critical("No valid com port found!!!")
            sys.exit(1)
            
        
        config_dict["usb"] = port
        
        config_named_tuple = collections.namedtuple('GenericDict', config_dict.keys())(**config_dict)
        
        
    