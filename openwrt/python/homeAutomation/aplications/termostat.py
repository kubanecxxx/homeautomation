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


def log_temperature(base,pipe,load,table):
    if (len(load) != 2):
        return

    teplota = base.getInt(load) / 2.0
    base._log.debug(log_to_db(base,pipe,teplota,table,"value","temperatures",True))
    base._log.debug(teplota)
        
    
class app(baseClass):
    def __init__(self,name):
        baseClass.__init__(self,name)
        
        #individual basic setup
        self.vmt[Hardware.NEW_DATA] = self.new_data
        self.vmt[Hardware.TX_FINISHED] = self.cosi
        #self.vmt[Hardware.TX_FAILED] = self.err
        self._pipe_list = [1]

        self.i = 0
        self._idle_count = 0
        #logging.getLogger("root.dispatcher").setLevel(logging.ERROR)        
                
        #logging.getLogger("root.serialHardware").setLevel(logging.ERROR)    
        
    def _idle_data(self,send,table,pipe,command,load):
        
        FORMAT = '%(asctime)s  [%(name)s]:[%(levelname)s] - %(message)s'
        formater= logging.Formatter(FORMAT)
        
        self._log.handlers = []
        self._log.setLevel(logging.NOTSET)
        
        try:
            fh = logging.FileHandler("/dev/pts/0",'w')
            fh.setFormatter(formater)
            fh.setLevel(logging.DEBUG)
                        
            if len(self._log.handlers) == 0:
                self._log.addHandler(fh)
                self._log.setLevel(logging.INFO)
        except:
            pass
        
        #send(pipe, table.KOTEL_TOPIT,0,1)
        #tady rozhodovat treba kazdej desatej poslat jesli topit nebo ne
        
        self._log.debug("idle from pipe %d" % pipe)
        #send(table.PIPE_KOTEL,table.MCU_RESET)
        #print_pts("idle from pipe %d" % pipe)
        
        if (self._idle_count > 10):
            con = mdb.connect(table.db_address,table.db_name,table.db_pass,"pisek")
            cur = con.cursor()
            cur.execute("select sp_topit()");
            topit = cur.fetchone()
            con.close()
            topit = topit[0]
            #self._log.warn("topit %d" % topit)
            self._log.info("topit %d" % topit)
            send(table.PIPE_KOTEL,table.KOTEL_TOPIT,topit,1)
            self._idle_count = 0
        
        self._idle_count += 1
            
        return
    
    def _new_temperature(self,send,table,pipe,command,load):
        (log_temperature(self,pipe, load, table))
        pass
   
    def _new_cerpadlo(self,send,table,pipe,command,load):
        if len(load) != 1:
            self._log.warning("cerpadlo new data - bad load length")
            return;
        
        
        enabled = load[0] & 1
        heating = (load[0] >> 1) & 1
        heating_latch = (load[0] >> 2) &1
        
        i = "new cerpadlo %d, heating %d, latch %d" % (enabled,heating,heating_latch)
        self._log.info(i)
            
        self._log_event_to_db(pipe, table, enabled,302)
        self._log_event_to_db(pipe,table, heating,301 )
        self._log_event_to_db(pipe,table, heating_latch,303 )
        #send(table.PIPE_KOTEL,table.MCU_RESET)
        
   
    def new_data(self,args):
        dispatcher = args[0]
        table = dispatcher.command_table()
        self._command_table[table.IDLE] = self._idle_data
        self._command_table[table.KOTEL_CERPADLO] = self._new_cerpadlo
        self._command_table[table.KOTEL_TEMPERATURE] = self._new_temperature
#        logging.getLogger("root").setLevel(logging.INFO)
        self._command_handler(args)
        
             
    def cosi(self,args):
        self._log.info(str(args))
        
        pass
    
    def err(self,args):
        print args
        
