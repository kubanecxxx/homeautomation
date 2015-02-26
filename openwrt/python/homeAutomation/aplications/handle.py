'''
Created on 30. 3. 2014

@author: kubanec
'''

from hardware.serialHardware import Hardware
from aplications.baseClass import baseClass, log_to_db,print_pts
from dispatcher.commandTable import commands
from dispatcher.dispatcher import dispatcher
import logging
import array
import time
import MySQLdb as mdb
from dispatcher import commandTable
import threading
import logging.handlers
import Queue
import library.stoppableThread
import datetime
from aplications.termostat import log_temperature

def getList(arr):
    list = []
    for idx in range(0,len(arr),2):
        e = array.array('B')
        e.append(arr[idx])
        e.append(arr[idx+1])
        int = baseClass.getInt(e)
        if int > 32767:
            int ^= 0xffff
            int += 1
            int *= -1
        list.append(int)
    return list

def toArray(lst):
    tmp = []
    for a in lst:
        tmp.append(int(a))

    arr = array.array('B')
    for a in tmp:
        b = a & 0xff
        c = (a >> 8) & 0xff
        arr.append(b)
        arr.append(c)
    
    return arr

def hoursMinutes(input):
    input = input.seconds / 60
    minutes = input % 60
    hours = input / 60 
    return (hours,minutes)
#napsat neco podobnyho obracene
                
                
def setup_heating(data_in, cursor):
    if len(data_in) == 6:
        weekend = True
    elif len(data_in ) == 12:
        weekend = False
    else:
        return
    
    m = []
    for idx,d in enumerate(range(0,len(data_in),3)):
        h = data_in[d]
        m = data_in[d+1]
        t = data_in[d+2]
        tm = datetime.time(h,m)
        query = "call sp_configureProgram(3,%f,\"%s\",NULL,%d,%d)" %(t,tm,weekend,idx)
        cursor.execute(query) 
    
class lest():
    names = {}
    names[0] = "main"
    names[1] = "heating week part1"
    names[2] = "heating weekend"
    names[3] = "water"
    names[4] = "heating week part2"
    names[5] = "maximum water tempearture"
    
    
    def __init__(self,name,function):
        self.lst = []
        self._old_lst = []
        self._function = function
        
        if name > 5:
            raise ValueError
        
        if name < 0:
            raise ValueError
        
        self._name = name
    
    @property
    def name(self):
        return self._name
    
    def name_string(self):
        return lest.names[self._name]
    
    def changed(self):
        if self._old_lst != self.lst:
            self._old_lst = self.lst
            return True
        
        return False
        
class app(baseClass):
    def __init__(self,name):
        baseClass.__init__(self,name)
        
        #individual basic setup
        #self.vmt[Hardware.TX_FAILED] = self.err
        self._pipe_list = [7]

        self.i = 0
        self._idle_count = 0
        
        #logging.getLogger("root.dispatcher").setLevel(logging.ERROR)        
        self._reload_screens = threading.Event()
        self._reload_screen = Queue.Queue()
                
                
        FORMAT = '%(asctime)s  [%(name)s]:[%(levelname)s] - %(message)s'
        formater= logging.Formatter(FORMAT)
        #fh = logging.FileHandler("/dev/pts/1",'w')
        #fh.setFormatter(formater)
        #fh.setLevel(logging.DEBUG)
        
        self._log.handlers = []
        self._log.setLevel(logging.NOTSET)
        #if len(self._log.handlers) == 0:
        #    self._log.addHandler(fh)
        #    self._log.setLevel(logging.INFO)

        
            
        self.fronta = Queue.Queue(1)
        self._screen_queue = Queue.Queue()
        
        for t in threading.enumerate():
            if t.name == "handle_mysqlthread":
                self._log.debug("stopping thread: " + str(t))
                t.stop()
                                
        self._thread = library.stoppableThread.stoppableThread( target=self.thd, name="handle_mysqlthread")
        self._thread.setDaemon(True)
        self._thread.start()
        
        self._thd_count = 0
        self._id = 0
        
    
    
    
    def virtual_new_data(self, dispatcher, pipe, command, payload):    
        table = dispatcher.command_table()
        self._command_table[table.IDLE] = self._idle_data
        self._command_table[table.HANDLE_MAIN_SCREEN] = self._new_main_screen
        self._command_table[table.HANDLE_WATER_SCREEN] = self._new_water_screen
        self._command_table[table.HANDLE_HEATING_SCREEN] = self._new_heating_screen
        self._command_table[table.HANDLE_GET_SCREENS] = self._new_get_screens
        self._command_table[table.HANDLE_PROGRAM_MANUAL] = self._new_program
        self._command_table[table.HANDLE_HOME_TEMPERATURE] = self._new_home_temperature
#        logging.getLogger("root").setLevel(logging.INFO)
        self._command_handler(dispatcher, pipe, command, payload)
                             
        
    def _prepare_heating_screen_week_p1(self,table):
        return self._prepare_heating_screen(table, False)
    def _prepare_heating_screen_week_p2(self,table):
        return self._prepare_heating_screen(table, False,2)
    def _prepare_heating_screen_weekend(self,table):
        return self._prepare_heating_screen(table, True)
    
    def thd(self):
        zoznam = []
        zoznam.append(lest(0,self._prepare_main_screen))
        zoznam.append( lest(1,self._prepare_heating_screen_week_p1))
        zoznam.append( lest(2,self._prepare_heating_screen_weekend)) 
        zoznam.append( lest(3,self._prepare_water_screen))
        zoznam.append(lest(5,self._prepare_water_temp))
        zoznam.append( lest(4,self._prepare_heating_screen_week_p2))
              
        self._log.debug("thread start")
        while not threading.current_thread().stopped():            
            #clear all data from lists to make it reload again and insert into queue
            if self._reload_screens.is_set():
                self._reload_screens.clear()
                for a in zoznam:
                    a._old_lst = []
             
            if self.fronta.empty():
                time.sleep(1)
            else:
                try:
                    table = self.fronta.get_nowait()
                    self._log.debug("have table")
                    
                    if not self._reload_screen.empty():
                        s = self._reload_screen.get()
                        mapa = {}
                        mapa[table.HANDLE_RELOAD_MAIN_SCREEN] = [0]
                        mapa[table.HANDLE_RELOAD_HEATING_SCREEN_WEEK] = [1,4]
                        mapa[table.HANDLE_RELOAD_HEATING_SCREEN_WEEKEND] = [2]
                        mapa[table.HANDLE_RELOAD_WATER_SCREEN] = [3,5]
                        lst = mapa[s]
                        for a in zoznam:
                            if a._name in lst:
                                a._old_lst = []
                                self._log.info("thd new screen request \"%s\" screen" % (a.name_string()))
                 
                 
                    for a in zoznam:
                        lst = a._function(table)
                        a.lst = lst
                        self._log.debug(a.name_string()+ " screen list fetched: " + str(a.lst))
                        if a.changed():
                            self._log.debug(a.name_string()+ " screen list changed: " + str(a.lst))
                            self._screen_queue.put(a)
                            pass
                
                    
                    self._thd_count += 1
                    self._log.debug("thread cycles count %d" % self._thd_count)
                    time.sleep(10)

                except:
                    self._log.exception("mysql model thread raised exception")
                    pass
        self._log.debug("thread stop")
        
    def _idle_data(self,send,table,pipe,command,load):
        self._log.debug("new idle command")
        try:
            self.fronta.put_nowait(table)
        except:
            pass
        
        if not self._screen_queue.empty() and self._id > 3:
            screen = self._screen_queue.get_nowait()
            self._send_data_screen(pipe, send, table, screen)
            self._id = 0
        
        self._id += 1
            
        return
    
    def _new_get_screens(self,send,table,pipe,command,load):
        self._log.debug("new get screens")
        
        if len(load) == 1:
            self._log.debug(load)
            a = load[0]
            self._reload_screen.put(a)
            pass
        elif len(load) == 0:
            self._reload_screens.set()
        
       
    def _new_home_temperature(self,send,table,pipe,command,load):        
        lst = getList(load)
        temp = lst[0] / 2.0
        self._log.info("new home temperature %f" % temp)
        log_temperature(self,pipe,load,table)
        
    def _new_program(self,send,table,pipe,command,load):
        lst = getList(load)
        t = lst[0] / 2.0
        p = lst[1]        
        self._log.debug("new program %d, manual temp %f" %(p,t))
        
        query = "call sp_selectProgram(%d)" % p
        self._log.debug(query)
        q2 = "update programy set teplota = %f where id = 1" % t
        self._log.debug(q2) 

        con = self._get_connection(table)
        cur = con.cursor()
        cur.execute(q2)
        cur.execute(query)
        con.close()
        
        
    def _new_main_screen(self,send,table,pipe,command,load):
        self._log.debug("new main screen data")
         
        a = getList(load)
        self._log.debug(str(a))
        
        #vytvorit podporu v databazi pro tyhle veci
        #nastavit program
        #nastavit manualni teplotu
        #logovat domaci teplotu
        

    def _new_water_screen(self,send,table,pipe,command,load):
        self._log.debug("new water screen")
        #nastavit databazi pro vodu
        lst = getList(load)
        self._log.debug(str(lst))
        
        c = 0
        con = self._get_connection(table)
        cur = con.cursor()
        for a in range(0,8,4):
            start = datetime.time(lst[a],lst[a+2]) 
            stop = datetime.time(lst[a+1],lst[a+3])
            query = "call sp_configureProgram(2,%f,\"%s\",\"%s\",NULL,%d)" %(lst[-1]/2,start,stop,c)
            c += 1
            self._log.debug(query)
            cur.execute(query)
            
        con.close()
        pass
    
        
    def _new_heating_screen(self,send,table,pipe,command,load):
        self._log.debug("new heating screen")
        lst = getList(load)
        self._log.debug(str(lst))
        
        c = 0
        if len(lst) == 12:
            weekend = False
        elif len(lst) == 6:
            weekend = True
        else:
            self._log.warning("new heating screen wrong packet length")
            return
        
        con = self._get_connection(table)
        cur = con.cursor()
            
        for a in range(0,len(lst),3):
            start = datetime.time(lst[a],lst[a+1]) 
            query = "call sp_configureProgram(3,%f,\"%s\",NULL,%d,%d)" %(lst[a+2]/2,start,weekend,c)
            c += 1
            self._log.debug("heating screen query: " +query)
            cur.execute(query)    
        #nastavit databazi pro topeni 
        
        con.close()
        pass
   
    
    def _send_data_screen(self,pipe,send,table,screen):
        
        ja ={}
        ja[0] = table.HANDLE_MAIN_SCREEN
        ja[1] = table.HANDLE_HEATING_SCREEN
        ja[2] = table.HANDLE_HEATING_SCREEN
        ja[3] = table.HANDLE_WATER_SCREEN
        ja[4] = table.HANDLE_HEATING_SCREEN
        ja[5] = table.HANDLE_WATER_SCREEN
        command = ja[screen.name]
        data = toArray(screen.lst) 

        self._log.info("screen to be send: " + screen.name_string() + "; command " + str(command) + "; " + str(data))            
        send(pipe,command,data)    
        
    
    def _get_connection(self,table):
        con = mdb.connect(table.db_address,table.db_name,table.db_pass,"pisek")
        return con
   
    def _prepare_main_screen(self,table):
        t = 0.01
        lst = []
        lst.append(time.localtime().tm_hour)
        lst.append(time.localtime().tm_min)
        lst.append(time.localtime().tm_wday)
        con = self._get_connection(table)
        cur = con.cursor()
        cur.execute("select sp_program()")
        program = cur.fetchone()        
        program = program[0]
        lst.append(program)
        time.sleep(t)
        #con.close()
        
           
        #con = self._get_connection(table)
        cur = con.cursor()
        cur.execute("call sp_getProgramyNames")
        cur.fetchone()
        man = cur.fetchone()
        man = man[2] * 2
        cur.fetchone()
        heat = cur.fetchone()
        heat = heat[2] * 2
        lst.append(heat)
        lst.append(man)
        lst.append(0)
        time.sleep(t)
        #con.close()
        
        #con = self._get_connection(table)
        cur = con.cursor()
        cur.execute("select  value from temperatures where cas = (select cas from temperatures where sensor = 201 order by cas desc limit 1)")
        water = cur.fetchone()
        water = water[0] * 2
        time.sleep(t)
        #con.close()

        lst.append(water)

        
        #con = self._get_connection(table)
        cur = con.cursor()
        cur.execute("select event from events where (pipe = 201 and event_id = 300) order by cas limit 1")
        ja = cur.fetchone()
        time.sleep(t)
        #con.close()
        alive = ja[0]
        lst.append(alive)
     
        
        #con = self._get_connection(table)
        cur = con.cursor()
        cur.execute("select sp_topit()");
        topit = cur.fetchone()
        topit = topit[0]
        lst.append(topit)
        time.sleep(t)
        con.close()
        
        return lst
    
    def _prepare_heating_screen(self,table,weekend,part=1):
        lst = []
        
        con = self._get_connection(table)
        cur = con.cursor() 
        query = "select start,teplota from programy where id = 3 and weekend =%d order by number asc limit 3" % weekend
        if part == 2:
            query = "select start,teplota from programy where id = 3 and weekend =0 order by number desc limit 1"  
        cur.execute(query);
        con.close()

        k = cur.fetchone()
        while k:
            tm = k[0] 
            temperature = k[1]
            
            hours,minutes = hoursMinutes(tm)
            lst.append(hours)
            lst.append(minutes)
            lst.append(temperature*2)
            
            k = cur.fetchone()
        return lst
    
    def _prepare_water_screen(self,table):
        lst = []
        
        con = self._get_connection(table)
        cur = con.cursor()
        query = "select start,stop from programy where id = 2" 
        cur.execute(query);
        con.close()

        k = cur.fetchone()
        while k:
            tm = k[0]
            tm2 = k[1]
            
            hours,minutes = hoursMinutes(tm)
            lst.append(hours)
            
            h2,m2 = hoursMinutes(tm2)
            lst.append(h2)
            lst.append(minutes)
            lst.append(m2)
            
            k = cur.fetchone()

        return lst
        
    def _prepare_water_temp(self,table):
        lst = []
    
        con = self._get_connection(table)
        cur = con.cursor()
        query = "select teplota from programy where id = 2 limit 1" 
        cur.execute(query);
        con.close()
    
        k = cur.fetchone()    
        lst.append(k[0]*2)
        
        return lst
 

        

