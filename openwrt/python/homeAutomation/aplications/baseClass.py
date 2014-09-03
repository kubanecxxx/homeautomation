'''
Created on 30. 3. 2014

@author: kubanec
'''

from hardware.serialHardware import Hardware
import logging
import threading
import array
import library.TimerReset
import MySQLdb as mdb
import fcntl
import datetime

def print_pts(text):
    try:
        fp = open("/dev/pts/1", 'w')
        fp.write(str(text) + "\r\n")
        fp.close()
    except:
        return
    
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


class baseClass:
    def __init__(self, name, autoResponseCheck = True):
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
        
        #self._timer = library.TimerReset.TimerReset(5,self._check_resp_timeout)
        #self._timer.setName(("check_response_timeout %s" % name))
        self._lock = threading.Lock()
        self._responding = False
        self._timer = None
        
        self._autoResponseCheck = autoResponseCheck
        #if autoResponseCheck:
        #    self._timer.start()        
    
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
        
        self._log_event_to_db(pipe, table, True, 300)
        #log_to_db(self, pipe, True, table,"zije","alive")
        if not ar:
            self._log.warning("Slave is alive now")
            
        
    def _check_resp_timeout(self,pipe,table):
        self._lock.acquire()
        self._responding = False
        self._lock.release()
        self._log.warning("Slave has not responded for 10 seconds")
        #log_to_db(self, pipe, False, table,"zije","alive")
        self._log_event_to_db(pipe, table, False, 300)
        pass
    
    @property
    def responding(self):
        self._lock.acquire()
        a = self._responding
        self._lock.release()
        return a
    
    @property
    def vmt(self):
        return self._vmt
    
    @property
    def pipe_list(self):
        return self._pipe_list
    
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


