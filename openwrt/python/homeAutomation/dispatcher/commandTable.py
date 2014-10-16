'''
Created on 30. 3. 2014

@author: kubanec
'''

import socket

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
    
        
    #termostat
    KOTEL_TOPIT = 100
    KOTEL_TEMPERATURE = 101
    KOTEL_CERPADLO = 102
    KOTEL_CERPADLO_TIMEOUT = 103

    #handle
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
    
    db_address = ""
    db_name = ""
    db_pass = ""
    
    db_address_list = {}
    db_name_list = {}
    db_pass_list = {}

    wrt = 'OpenWrt'
    pc = 'kubanec-linux'
    db_address_list[wrt] = "localhost"
    db_address_list[pc] = "192.168.1.1"
    db_name_list[wrt] = "root"
    db_name_list[pc] = "kubanec"
    db_pass_list[wrt] = "heslo"
    db_pass_list[pc] = "kokot"
    
    def __init__(self):
        name = socket.gethostname()
        self.db_address = self.db_address_list[name]
        self.db_name = self.db_name_list[name]
        self.db_pass = self.db_pass_list[name]
