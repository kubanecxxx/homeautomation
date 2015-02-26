##
# @defgroup User_modules
# @brief User space for creating his own modules to operate with slave wireless modules
# @{


from hardware.serialHardware import Hardware
import logging
import threading
import array
import library.TimerReset
import MySQLdb as mdb
import fcntl
import datetime

##
# @brief debugging function to print data to another terminal
# @deprecated
def print_pts(text):
    try:
        fp = open("/dev/pts/1", 'w')
        fp.write(str(text) + "\r\n")
        fp.close()
    except:
        return
    
##
# @brief helper function to log whatever into database if value is different 
# then before 
# @details
# struct of the table in database:
# | timestamp | ID | pipe | event | event_id |
# <br> timestamp and ID are processed automatically by database
# 
# @todo forbid temperature table and transfer its data to events table
#
# @param base instance of caller class which inherits from @ref baseClass
# @param pipe [int] logical address of wireless module written to "pipe" column
# @param value [float] this value will be stored in "event" column
# @param table [@ref command_table] table is needed to decode pipe identificator
# @param parameter [string] name of "event" column
# @param db_table [string] name of the table in database
# @param tolerance [boolean] useful when logging temperature because 
# the value moves by 0.5 degree down and up in short time. The value will be logged 
# after two minutes if the new value is 0.5 degree different then previous value
#
# @deprecated use @ref baseClass method
def log_to_db(base,pipe,value,table,parameter,db_table, tolerance = False):
    #writes data to database if value is different from last sample 
    
    idd = table.stations_db_ids[pipe]
    con = mdb.connect(table.db_address,table.db_name,table.db_pass,"pisek") 
    cur = con.cursor()
    query = "select cas,%s from %s where cas=(select max(cas) from %s where sensor=%d)" \
    % (parameter,db_table,db_table,idd)
    cur.execute(query)

    q = "insert into %s(%s,sensor) values(%s,%d)" % (db_table,parameter,value,idd)
    query = None
    a = cur.fetchone()
    now = datetime.datetime.now()
    if a:
        cas = a[0]
        _zije = a[1]
        if _zije != value:
            if tolerance:
                if not( (_zije + 0.5) >= value and  value >= (_zije - 0.5)) \
                 or (cas + datetime.timedelta(minutes=2)) < now:
                    query = q
            else:
                query = q
    else:
        query = q
             
    if query:
        cur.execute(query)
    con.close()
    
    return query


##
# @brief main super class of all user modules 
# User module class definition must be like <b>def class app(@ref baseClass)</b>, 
# class name <b>app</b> is mandatory because @ref dispatcher searches for the
# class name app
#
# main purposes are:
#   + Creates subclass logger by module name
#   + Optionaly checks if asociated wireless slave module is alive (timeout)
#   + Distribution wireless commands via table of methods - user doesn't need to test 
#   wireless command code in subclass. Module methods are called instead.
class baseClass:
    ##
    # @brief initialise logger by subclass name
    def __init__(self, name, autoResponseCheck = True):
        ## @brief @ref dispatcher_codes asociated dictionary to functions/methods to be called
        # when data from asociated wireless module are received/tx finished or error occurs
        # key is @ref serial_commands and value is method or function
        # @details dictionary should look like this: 
        # <br> @serparam
        # by default all is set to None, when function/method is set to None it cannot be called
        # @todo destroy it and use normal virtual function overriding instead with normal parameters  not tuple
        self._vmt = {
                     Hardware.NEW_DATA : None,  # (dispatcher_instance, pipe, application_command, data)
                     Hardware.ERROR : None,  # (dispatcher_instance, error_code)
                     Hardware.TX_FAILED : None,  # (dispatcher_instance, pipe, application_command, data)
                     Hardware.TX_FINISHED : None  # (dispatcher_instance, pipe)
                     }
        ## @brief user module name is taken from filename by dispatcher
        self._name = name
        ## @brief asociated wireless modules with user module, when new data or other
        # event occurs functions specified in @ref _vmt are called. If the pipe is not 
        # listed here functions will not be called.
        self._pipe_list = []
        self._log = logging.getLogger("root.apps." + name)
        self._log.info("Instance created: %s", name)
        
        #self._timer = library.TimerReset.TimerReset(5,self._check_resp_timeout)
        #self._timer.setName(("check_response_timeout %s" % name))
        self._lock = threading.Lock()
        self._responding = False
        self._timer = None
        
        self._autoResponseCheck = autoResponseCheck
        #if autoResponseCheck:
        #    self._timer.start()        
    
        ## @brief command_code to function dictionary @ref command_table is a key 
        # and module function is value 
        # 
        # function style must be like this:
        # method(function_for_sending_wireless_data, command_table, pipe, command, payload)       
        # 
        self._command_table = {};
        self._log.handlers = []
        self._log.setLevel(logging.NOTSET)
    
    def _log_event_to_db(self,pipe,table,event_value,event_id,tolerance = False):
        #writes data to database if value is different from last sample 
        idd = table.stations_db_ids[pipe]
        con = mdb.connect(table.db_address,table.db_name,table.db_pass,"pisek") 
        cur = con.cursor()
        query = "select cas,event from events where event_id = %d and pipe = %d order by cas desc limit 1" % (event_id, idd)         
        cur.execute(query)
    
        q = "insert into events(pipe,event,event_id) values(%d,%s,%d)" % (idd,event_value,event_id)
        query = None
        a = cur.fetchone()
        now = datetime.datetime.now()
        if a:
            cas = a[0]
            _zije = a[1]
            if _zije != event_value:
                if tolerance:
                    if not( (_zije + 0.5) >= event_value and  event_value >= (_zije - 0.5)) \
                     or (cas + datetime.timedelta(minutes=2)) < now:
                        query = q
                else:
                    query = q
            if (cas + datetime.timedelta(hours=2)) < now:
                query = q
        else:
            query = q
                 
        if query:
            cur.execute(query)
        con.close()
        
        return query
    
    ##
    # @brief checks if asociated wireless slave module is alive
    # 10 seconds timeout no data from module
    #
    # if situation changes event will be logged into database by pipe number
    # with event code 300
    # @todo event codes into command_table
    def _check_response(self,pipe,table):    
        #self._timer.reset(5)
        if self._timer:
            self._timer.cancel()
        self._timer = threading.Timer(10,self._check_resp_timeout,[pipe,table])
        self._timer.setName(("check_response_timeout %s") %self._name)
        self._timer.start()
        self._lock.acquire()
        ar = self._responding
        self._responding = True
        self._lock.release()
        
        #event is internally logged after two hours if there is no change
        self._log_event_to_db(pipe, table, True, 300)
        #log_to_db(self, pipe, True, table,"zije","alive")
        if not ar:
            self._log.warning("Slave is alive now")
            
    ##
    # @brief @ref _check_response timer callback 
    # if the callback is called slave has not responded for 
    # specified time (10 seconds) and event is logged into database
    def _check_resp_timeout(self,pipe,table):
        self._lock.acquire()
        self._responding = False
        self._lock.release()
        self._log.warning("Slave has not responded for 10 seconds")
        #log_to_db(self, pipe, False, table,"zije","alive")
        self._log_event_to_db(pipe, table, False, 300)
        pass
    
    ##
    # @brief slave state 
    # @return slave status
    @property
    def responding(self):
        self._lock.acquire()
        a = self._responding
        self._lock.release()
        return a
    
    ## @brief returns @ref serial_commands functions dictionary
    @property
    def vmt(self):
        return self._vmt
    
    ## @brief returns list of asociated wireless modules
    @property
    def pipe_list(self):
        return self._pipe_list
    
    ##
    # @brief conversion function from array of character
    # creates integer 
    # @param arr [array.array("c")] input byte array
    # @return arr converted to integer
    @staticmethod
    def getInt(arr):
        if type(arr) is not array.array:
            raise ValueError
        
        t = 0
        arr.reverse()
        for j in arr:
            t <<= 8
            t |= j & 0xff
            
        return t
    
    ##
    # @brief this method is called by subclass in wireless recieved data callback
    # and according to @ref _command_table asociated function is called 
    # @param args [tuple(dispatcher, pipe, command, payload)]
    #   + dispatcher - dispatcher instance 
    #   + pipe - wireless data received from pipe
    #   + command - command code @ref command_table
    #   + payload - data
    def _command_handler(self, args):
        # @type dispatcher: dispatcher
        # @type pipe: int
        # @type command: int
        # @type payload: array.array("B")
        
        dispatcher,pipe,command,payload = args
        table = dispatcher.command_table()
        send_function = dispatcher.send_packet
        t = command | table.WRITE_FLAG
        
        if self._autoResponseCheck:
            self._check_response(pipe,table)
        
        self._log.debug("new command  %d, load %s" % (command,payload))
        if self._command_table.has_key(t):
            f = self._command_table[t]
            f(send_function,table,pipe,command,payload)
            return
            
        t = command & (~table.WRITE_FLAG & 0xffff)
        if self._command_table.has_key(t):
            f = self._command_table[t]
            f(send_function,table,pipe,command,payload)


## @}
