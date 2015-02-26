import socket

##
# @addtogroup dispatcher_package
# @{

##
# @defgroup command_table
# @brief message system commands
# @{

##
# @brief commands for message system between wireless modules and this 
# controlling application
#
# basically the same table is used in wireless modules but those modules
# are written in C/C++ so there it is enum
class commands:    
    REFRESH_PERIOD = 0.5
    
    
    #slave wants to read value
    READ_FLAG = 0x0000
    #slave wants to write value
    #master write value to slave
    WRITE_FLAG = 0x8000
    
    # commands
    IDLE = 0xffff
    STARTUP = 10000
    MCU_RESET = 10001
    
    #basic time commands
    TIME_HOURS = 1
    TIME_MINUTES = 2
    TIME_SECONDS = 3
    
    DATE_DAY = 4
    DATE_MONTH = 5
    DATE_YEAR = 6
    DATE_WEEK_DAY = 7
    DATE_YEAR_DAY = 8
    TIME_SINCE_EPOCH = 9
    
        
    #termostat section
    KOTEL_TOPIT = 100
    KOTEL_TEMPERATURE = 101
    KOTEL_CERPADLO = 102
    KOTEL_CERPADLO_TIMEOUT = 103

    #GUI handle section
    HANDLE_MAIN_SCREEN = 200
    HANDLE_WATER_SCREEN = 201
    HANDLE_HEATING_SCREEN = 202
    HANDLE_GET_SCREENS = 210
    HANDLE_HOME_TEMPERATURE = 220
    HANDLE_PROGRAM_MANUAL = 221
    HANDLE_RELOAD_MAIN_SCREEN = 50
    HANDLE_RELOAD_HEATING_SCREEN_WEEK = 51
    HANDLE_RELOAD_HEATING_SCREEN_WEEKEND = 52
    HANDLE_RELOAD_WATER_SCREEN = 53


    #pipe list section
    PIPE_KOTEL = 1
    PIPE_OVLADAC = 0
    PIPE_HODINY = 2
    

    stations_db_ids = {}
    stations_db_ids[PIPE_KOTEL] = 201
    stations_db_ids[PIPE_OVLADAC] = 200
    stations_db_ids[PIPE_HODINY] = 202
    
    
    stations = {}
    stations[PIPE_KOTEL] = "kotel"
    stations[PIPE_OVLADAC] = "ovladac"
    stations[PIPE_HODINY] = "hodiny"
    
    #database connection section
    db_address = ""
    db_name = ""
    db_pass = ""
    
    db_address_list = {}
    db_name_list = {}
    db_pass_list = {}

    wrt = 'OpenWrt'
    pc = 'kubanec-linux'
    ntbk = 'kubanec-laptop'
    db_address_list[ntbk] = "localhost"
    db_address_list[wrt] = "localhost"
    db_address_list[pc] = "192.168.1.1"
    db_name_list[wrt] = "root"
    db_name_list[pc] = "kubanec"
    db_name_list[ntbk] = "kubanec"
    db_pass_list[wrt] = "heslo"
    db_pass_list[pc] = "kokot"
    db_pass_list[ntbk] = "kokot"
    
    ##
    # @brief According to the hostname select database credentials
    #
    # used mainly for testing reasons - main development was on PC and
    # the application used to connect directly to the database from the PC.
    # Then it runs directly on openwrt router which also contains the MySQL database
    # 
    # @warning these values must be set according to your database parameters 
    # @todo use configuration file
    def __init__(self):
        name = socket.gethostname()
        self.db_address = self.db_address_list[name]
        self.db_name = self.db_name_list[name]
        self.db_pass = self.db_pass_list[name]


#@}
#@}
