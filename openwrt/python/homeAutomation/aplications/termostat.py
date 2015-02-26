##
# @defgroup User_modules
# @{ 

from hardware.serialHardware import Hardware
from aplications.baseClass import baseClass, log_to_db,print_pts
from dispatcher.commandTable import commands
from dispatcher.dispatcher import dispatcher
import logging
import array
import time
import MySQLdb as mdb
from dispatcher import commandTable

##
# @brief helper function to log temperature recieved from wireless slave module
# to database
def log_temperature(base,pipe,load,table):
    if (len(load) != 2):
        return

    teplota = base.getInt(load) / 2.0
    base._log.debug(log_to_db(base,pipe,teplota,table,"value","temperatures",True))
    base._log.debug(teplota)
        
    
##
# @brief termostat module class
class app(baseClass):
    def __init__(self,name):
        baseClass.__init__(self,name)
    
        ## @brief asociated wireless module has logical address 1
        self._pipe_list = [1]

        self.i = 0
        self._idle_count = 0
        #logging.getLogger("root.dispatcher").setLevel(logging.ERROR)        
                
        #logging.getLogger("root.serialHardware").setLevel(logging.ERROR)    
        
    ##
    # @wireless
    #
    # @brief idle_data 
    # every 5 idle packets received is checked from database if heating
    # should be enabled or disabled and this information is sent to the 
    # hardware
    def _idle_data(self,send,table,pipe,command,load):
        self._log.debug("idle from pipe %d" % pipe)
        #send(table.PIPE_KOTEL,table.MCU_RESET)
        #print_pts("idle from pipe %d" % pipe)
        
        if (self._idle_count > 5):
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
    
    ##
    # @wireless
    #
    # @brief temperature of water in hot water container
    # 
    # temperature is logged into the database
    def _new_temperature(self,send,table,pipe,command,load):
        (log_temperature(self,pipe, load, table))
        pass
   
    ## 
    # @wireless
    #
    # @brief state of binary inputs and outputs (cerpadlo means water pump in
    # czech language
    #
    # load contains these common data:
    #   + water pump state (disabled/enabled) bit 0
    #   + heating status (really burns or not - taken directly from heating via
    #   optocoupler) bit 1
    #   + heating relay output latch (latch from the microprocessor output) it
    #   is used for debugging  bit 2
    #   + upper two bytes contains remaing time in seconds when heating should
    # be turned off automatically by microcontroller timeout - if
    # microcontroller does not recieve command to enable heating it will
    # automatically disable heating after 6 minutes.
    #
    # states of those binary inputs/outputs are logged into database
    def _new_cerpadlo(self,send,table,pipe,command,load):
        if len(load) != 4:
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
        
        a = load[2:]
        ch = baseClass.getInt(a)
        if heating_latch:
            i = "disable time remains [seconds] %d " % ch
            logging.getLogger("root.superSpecial").info(i)
            
        
    ##
    # @base_virtual
    #
    # @brief new wireless data received 
    # prepare @ref baseClass._command_table and call @ref baseClass._command_handler
    def virtual_new_data(self, dispatcher, pipe, command, payload):
        table = dispatcher.command_table()
        self._command_table[table.IDLE] = self._idle_data
        self._command_table[table.KOTEL_CERPADLO] = self._new_cerpadlo
        self._command_table[table.KOTEL_TEMPERATURE] = self._new_temperature
#        logging.getLogger("root").setLevel(logging.INFO)

        self._command_handler(dispatcher,pipe,command,payload)
        

## @}
