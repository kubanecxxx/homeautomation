'''
Created on 30. 3. 2014

@author: kubanec
'''

class commands:    
    REFRESH_PERIOD = 0.5
    
    
    #slave wants to read value
    READ_FLAG = 0x0000
    #slave wants to write value
    #master write value to slave
    WRITE_FLAG = 0x8000
    
    # commands
    IDLE = 0
    
    #basic time commands
    TIME_HOURS = 1
    TIME_MINUTES = 2
    TIME_SECONDS = 3
    
    DATE_DAY = 4
    DATE_MONTH = 5
    DATE_YEAR = 6
    DATE_WEEK_DAY = 7
    DATE_YEAR_DAY = 8
    
    
    
    
