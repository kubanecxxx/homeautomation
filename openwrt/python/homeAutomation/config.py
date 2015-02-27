import ConfigParser
import collections

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
        config_dict["usb"] = p.get("serial", "usb")
        config_dict["baudrate"] = p.getint("serial","baudrate")
        config_dict["db_name"]  = p.get("database","name")
        config_dict["db_password"]  = p.get("database","password")
        config_dict["db_host"]  = p.get("database","host")
        config_dict["db_database"] = p.get("database","database_name")
        config_dict["logging_control_port"] = p.getint("logging","control_port")
        
        config_named_tuple = collections.namedtuple('GenericDict', config_dict.keys())(**config_dict)