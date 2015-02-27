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
    

    ## 
    # @brief station ids dictionary by the database table
    stations_db_ids = {}
    stations_db_ids[PIPE_KOTEL] = 201
    stations_db_ids[PIPE_OVLADAC] = 200
    stations_db_ids[PIPE_HODINY] = 202
    
    ##    
    # @brief station names dictionary by the database table
    stations = {}
    stations[PIPE_KOTEL] = "kotel"
    stations[PIPE_OVLADAC] = "ovladac"
    stations[PIPE_HODINY] = "hodiny"
    
    ##
    # @brief database events id enum
    class event_id():
        SLAVE_ALIVE = 300
        HEATING_ENABLED = 301
        WATER_PUMP_ENABLED = 302
        HEATING_LATCH = 303
        WARM_WATER_TEMPERATURE = 304
        HOME_TEMPERATURE = 305
        pass

#@}
#@}
