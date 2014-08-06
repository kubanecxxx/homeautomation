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
        
class main_screen:
    size = 10
    
    hours = 0
    minutes = 1
    dayofweek = 2
    program = 3
    heatingTemperature = 4
    manualTemperature = 5
    homeTemperature = 6
    waterTemperature = 7
    slaveConnectionStatus = 8
    heatingActive = 9
    
        
    
class lest():
    names = {}
    names[0] = "main"
    names[1] = "heating week"
    names[2] = "heating weekend"
    names[3] = "water"
    
    
    def __init__(self,name,function):
        self.lst = []
        self._old_lst = []
        self._function = function
        
        if name > 3:
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
        self.vmt[Hardware.NEW_DATA] = self.new_data
        self.vmt[Hardware.TX_FINISHED] = self.cosi
        #self.vmt[Hardware.TX_FAILED] = self.err
        self._pipe_list = [0]

        self.i = 0
        self._idle_count = 0
        
        #logging.getLogger("root.dispatcher").setLevel(logging.ERROR)        
                
                
                
        FORMAT = '%(asctime)s  [%(name)s]:[%(levelname)s] - %(message)s'
        formater= logging.Formatter(FORMAT)
        fh = logging.FileHandler("/dev/pts/2",'w')
        fh.setFormatter(formater)
        fh.setLevel(logging.DEBUG)

        
        self._log.handlers = []
        #self._log.setLevel(logging.NOTSET)
        if len(self._log.handlers) == 0:
            self._log.addHandler(fh)
            self._log.setLevel(logging.INFO)
            
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
    
        
    def _prepare_heating_screen_week(self,table):
        return self._prepare_heating_screen(table, False)
    def _prepare_heating_screen_weekend(self,table):
        return self._prepare_heating_screen(table, True)
    
    def thd(self):
        zoznam = []
        zoznam.append(lest(0,self._prepare_main_screen))
        zoznam.append( lest(1,self._prepare_heating_screen_week))
        zoznam.append( lest(2,self._prepare_heating_screen_weekend))
        zoznam.append( lest(3,self._prepare_water_screen))
        
        
        self._log.debug("thread start")
        while not threading.current_thread().stopped():            
            if self.fronta.empty():
                time.sleep(1)
            else:
                try:
                    table = self.fronta.get_nowait()
                    self._log.debug("have table")

                 
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
        
        if not self._screen_queue.empty():
            screen = self._screen_queue.get_nowait()
            self._send_data_screen(pipe, send, table, screen)
            
        return
       
    def _new_main_screen(self,send,table,pipe,command,load):
        self._log.debug("new main screen data")
         
        a = getList(load)
        self._log.debug(str(a))
        
        #vytvorit podporu v databazi pro tyhle veci
        #nastavit program
        #nastavit manualni teplotu
        #logovat domaci teplotu
        
    def _new_water_screen(self,send,table,pipe,command,load):
        #nastavit databazi pro vodu
        pass
       
    def _new_heating_screen(self,send,table,pipe,command,load):
        #nastavit databazi pro topeni 
        pass
   
    
    def _send_data_screen(self,pipe,send,table,screen):
        
        ja ={}
        ja[0] = table.HANDLE_MAIN_SCREEN
        ja[1] = table.HANDLE_HEATING_SCREEN
        ja[2] = table.HANDLE_HEATING_SCREEN
        ja[3] = table.HANDLE_WATER_SCREEN
        command = ja[screen.name]
        data = toArray(screen.lst)
                
        self._log.debug("screen to be send: " + screen.name_string() + "; command " + str(command) + "; " + str(screen.lst))
        
        #send(pipe,command,data)
        
    
    def _get_connection(self,table):
        con = mdb.connect(table.db_address,table.db_name,table.db_pass,"pisek")
        return con
   
    def _prepare_main_screen(self,table):
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
        con.close()
        
        time.sleep(1)
        
        con = self._get_connection(table)
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
        con.close()
        
        time.sleep(1)
        
        con = self._get_connection(table)
        cur = con.cursor()
        cur.execute("select  value from temperatures where cas = (select cas from temperatures where sensor = 201 order by cas desc limit 1)")
        water = cur.fetchone()
        water = water[0] * 2
        con.close()
        lst.append(water)
        
        time.sleep(1)
        
        con = self._get_connection(table)
        cur = con.cursor()
        cur.execute("select zije from alive where sensor = 201 order by cas limit 1")
        ja = cur.fetchone()
        con.close()
        alive = ja[0]
        lst.append(alive)
     
        time.sleep(1)
        
        con = self._get_connection(table)
        cur = con.cursor()
        cur.execute("select sp_topit()");
        topit = cur.fetchone()
        topit = topit[0]
        lst.append(topit)
        
        return lst
    
    def _prepare_heating_screen(self,table,weekend):
        lst = []
        
        con = self._get_connection(table)
        cur = con.cursor()
        query = "select start,teplota from programy where id = 3 and weekend =%d order by number asc" % weekend 
        cur.execute(query);
        con.close()

        k = cur.fetchone()
        while k:
            tm = k[0]
            temperature = k[1]
            
            hours,minutes = hoursMinutes(tm)
            lst.append(hours)
            lst.append(minutes)
            lst.append(temperature)
            
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
            lst.append(minutes)
            h2,m2 = hoursMinutes(tm2)
            lst.append(h2)
            lst.append(m2)
            
            k = cur.fetchone()
        return lst
     
    def new_data(self,args):
        dispatcher = args[0]
        table = dispatcher.command_table()
        self._command_table[table.IDLE] = self._idle_data
        self._command_table[table.HANDLE_MAIN_SCREEN] = self._new_main_screen
        self._command_table[table.HANDLE_WATER_SCREEN] = self._new_water_screen
        self._command_table[table.HANDLE_HEATING_SCREEN] = self._new_heating_screen
#        logging.getLogger("root").setLevel(logging.INFO)
        self._command_handler(args)
        
             
    def cosi(self,args):
        pass
    
    def err(self,args):
        print args
        
