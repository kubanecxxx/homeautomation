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
import config 

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
# @todo transfer temperature to events
# @deprecated use @ref baseClass method instead
def log_to_db(base,pipe,value,table,parameter,db_table, tolerance = False):
    ## @type base: aplications.baseClass.baseClass
    ## @type pipe: int
    #writes data to database if value is different from the previous sample 
    
    idd = table.stations_db_ids[pipe]
    con = base.database_connect()
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
        ## @brief user module name is taken from filename by dispatcher
        self._name = name
        ## @brief asociated wireless modules with user module, when new data or other
        # event occurs virtual methods are called. If the pipe is not 
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

        cd = config.config_dict
        ## @brief database remote address read from config file
        self.db_host = cd["db_host"]
        ## @brief database user name read from config file
        self.db_user = cd["db_name"]
        ## @brief database user password read from config file
        self.db_pass = cd["db_password"]
        ## @brief database name to be used read from config file
        self.db_database = cd["db_database"]

    ## 
    # @defgroup Virtual_methods
    # @brief virtual methods set is overriden by subclasses of baseClass. It is API for
    # receiving callbacks from hardware layer. Default implementations just
    # create log message that the unimplemented function was called.
    # @{

    ##
    # @brief this method is supposed to be reimplemented by 
    # subclass to receive data from asociated wireless module
    # @param dispatcher instance of master @ref dispatcher.dispatcher.dispatcher
    # @param pipe [int] logical address of wireless slave module which sent the
    # packet
    # @param command [int] @ref command_table value 
    # @param payload [array.array("B")] payload data
    def virtual_new_data(self, dispatcher, pipe, command, payload):
        # @type dispatcher: dispatcher.dispatcher.dispatcher
        # @type pipe: int
        # @type command: int
        # @type payload: array.array("B")
        self._log.debug("unimplemented - default action; new data arrived")
        pass

    ##
    # @brief this method is supposed to be reimpelemted by 
    # subclass to receive information about data was sucesfully sent to 
    # wireless module
    # @param dispatcher instance of master @ref dispatcher.dispatcher.dispatcher
    # @param pipe [int] logical address of wireless slave unit which data was
    # successfully sent to
    def virtual_tx_finished(self, dispatcher, pipe):
        # @type dispatcher: dispatcher.dispatcher.dispatcher
        # @type pipe: int
        self._log.debug("unimplemented - default action; tx finished")
        pass
    ##
    # @brief this method is supposed to be reimpelemted by 
    # subclass to receive information about failed transmition to 
    # slave wireless module
    # @param dispatcher instance of master @ref dispatcher.dispatcher.dispatcher
    # @param pipe [int] logical address of wireless slave module
    # @param command [int] @ref command_table code
    # @param data [array.array("B")] payload
    def virtual_tx_failed(self,dispatcher, pipe, command, data):
        # @type dispatcher: dispatcher.dispatcher.dispatcher
        # @type pipe: int
        # @type command: int
        # @type data array.array("B")
        self._log.debug("unimplemented - default action; tx failed")
        pass

    ## 
    # @brief this method is supposed to be reimpelemted by 
    # subclass to receive information that error occured in hardware 
    # @param dispatcher instance of master @ref dispatcher.dispatcher.dispatcher
    # @param error_code [int] error code from @ref hardware
    def virtual_error(self,dispatcher, error_code):
        # @type dispatcher: dispatcher.dispatcher.dispatcher
        # @type error_code: int
        self._log.debug("unimplemented - default action ; error")
        pass
    
    ## @}
    
    ##
    # @brief helper function connect to the database and return opened 
    # database connection
    # @return database connection
    def database_connect(self):
        con = mdb.connect(self.db_host,self.db_user,self.db_pass,self.db_database) 
        return con

    ## 
    # @sa @ref log_to_db
    def _log_event_to_db(self,pipe,table,event_value,event_id, database_table = "events" , tolerance = False):
        #writes data to database if value is different from last sample 
        idd = table.stations_db_ids[pipe]
        con = self.database_connect()
        assert isinstance(con, mdb.connection)
        cur = con.cursor()
        query = "select cas,event from %s where event_id = %d and pipe = %d order by cas desc limit 1" % (database_table, event_id, idd)         
        cur.execute(query)
    
        q = "insert into %s(pipe,event,event_id) values(%d,%s,%d)" % (database_table,idd,event_value,event_id)
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
        self._log_event_to_db(pipe, table, True, table.event_id.SLAVE_ALIVE)
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
        self._log_event_to_db(pipe, table, False, table.event_id.SLAVE_ALIVE)
        pass
    
    def stop_timer(self):
        self._log.debug("stopping... timer")
        if self._timer:
            self._timer.cancel()
            self._log.debug("stopped timer")
    
    ##
    # @brief slave state 
    # @return slave status
    @property
    def responding(self):
        self._lock.acquire()
        a = self._responding
        self._lock.release()
        return a
    
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
    # @param dispatcher [@ref dispatcher.dispatcher.dispatcher] instance
    # @param pipe [int] logical address of wireless slave module which sent the packet
    # @param command [int] @ref command_table code of packet
    # @param payload [array.array("B")] packet arbitrary data
    def _command_handler(self, dispatcher, pipe, command, payload):
        # @type dispatcher: dispatcher
        # @type pipe: int
        # @type command: int
        # @type payload: array.array("B")
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


#@}
