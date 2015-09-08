
import sys
from hardware import serialHardware
from events import events
import logging
import logging.handlers
from dispatcher import dispatcher
import time
import config
import os
import single_instance
import tcp_shell.tcpShell
import signal
import threading

def sigterm(a,b):
    logging.getLogger("root").info("application terminated by SIGTERM")
    print "SIGTERM was sent"    
    tidy_up()
    pass

def tidy_up():
    print "bye"
    events.event.register_exit(0)    
    disp.close()
    shell.clean()
    print threading.enumerate()
    sys.exit(0)

## @brief setup logging facility
def _setup_logger():
    # setup logging facility
    FORMAT = '%(asctime)s  [%(name)s]:[%(levelname)s] - %(message)s'
    #logging.basicConfig(format=FORMAT)
    formater= logging.Formatter(FORMAT)
    
    import inspect 
    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
    
    fh = logging.handlers.RotatingFileHandler(path + "/log.txt",maxBytes=(1024*1024*1),backupCount=7)
    fh_error = logging.handlers.RotatingFileHandler(path + "/errors.txt",maxBytes=(1024*1024*1),backupCount=7)
    fh.setFormatter(formater)
    fh.setLevel(logging.WARN)
    fh_error.setFormatter(formater)
    fh_error.setLevel(logging.ERROR)
    cout = logging.StreamHandler(sys.stdout)
    cout.setFormatter(formater)
    cout.setLevel(logging.DEBUG)
    
    stderr = logging.StreamHandler(sys.stderr)
    stderr.setLevel(logging.WARN)
    
    a = logging.getLogger("root")
    a.addHandler(stderr)
    a.setLevel(1)
    
    logging.getLogger("root").addHandler(cout)
    
    #a.addHandler(cout)
    a.addHandler(fh)
    a.addHandler(fh_error)
    
    return a
            
if __name__ == '__main__':
    signal.signal(signal.SIGTERM,sigterm)
    signal.signal(signal.SIGINT,sigterm)
                
    parameter_list = ["pid-file"]
    input_pars = {}
    
    ## default parameters
    input_pars["pid-file"] = "/var/run/homeAutomation.pid"
    
    for a in sys.argv:
        for p in parameter_list:
            t = ("--" + p + "=")
            if t in a:
                a = a.replace(t,"")
                input_pars[p] = a
    
    
    pid_file = input_pars["pid-file"]
    
    ## setup logs
    a = _setup_logger()
    
    ## check if another instance of app is running
    single_instance.check_single_instance(pid_file)
    
    print "How are you doing everybody let's start "
    c = config.application_config("config.cfg")
    
    ## setup remote shell
    shell = tcp_shell.tcpShell.tcpShell(config.config_dict["logging_control_port"],"root")
    shell.start()
    
    a.warn("application started")
    
    # start the application 
    disp = dispatcher.dispatcher()
    disp.start()

    event_loop = threading.Thread(target=events.event.loop,name="event loop")
    event_loop.setDaemon(False)
    event_loop.start()
    
    try:
        while True:
            l = logging.getLogger("root.threads")
            time.sleep(1)
            i = 0
            for a in threading.enumerate():
                i += 1
                l.debug( "%d - %s" % (i,a)) 
    except KeyboardInterrupt:
        a.warn("application disabled by CTRL+C")
        tidy_up()    

    #th.join()
##
# @mainpage Application classes colaboraiton
#
# <h1>Class colaboration diagram</h1>
# @dot
# digraph classess {
# node[shape=record]
# hw[label="Hardware" URL = "@ref hardware"]
# event[label="Event loop" URL = "@ref events.events.event" shape=Mrecord]
# dispatcher[label="Dispatcher" URL = "@ref dispatcher.dispatcher.dispatcher"]
# base[label="Base class" URL = "\ref aplications.baseClass.baseClass"]
# user[label="User modules" URL = "@ref User_modules"]
#
# hw -> event-> dispatcher [label="Dispatcher codes callbacks \n through event loop " URL = "@ref dispatcher_codes"] 
# dispatcher -> user [label="Virtual methods" URL="@ref Virtual_methods"]
# user -> base [label="Inherits from"]
# } 
# @enddot
#
# <h1>Thread colaboration diagram</h1>
# @dot
# digraph threads {
# node [shape=record]
# subgraph clustermain_thread {
# main[label="Event loop" URL = "@ref events.events.event"]
# dispatcher[label="Dispatcher" URL = "@ref dispatcher.dispatcher.dispatcher"]
# user[label="User modules" URL = "@ref User_modules"]
# main -> dispatcher [label = "Queue pop"]
# dispatcher -> user [label = "Overriden methods" URL = "@ref Virtual_methods" ]
# label="Main thread"
# color=lightgrey
# } 
#
# subgraph clusterhardware {
# color=transparent
# recieving[label="Hardware data receiving\n and decoding thread" URL = "@ref hardware.serialHardware.Hardware"]
# sending[label="Wireless data sending thread" URL="@ref hardware.serialHardware.Hardware"]
# }
# 
# recieving -> main [label="Queue put"]
# dispatcher -> sending [label="Queue"] 
# }
# @enddot
#
# All user modules inherits from @ref aplications.baseClass.baseClass
# Base class distributes wireless data which are received through @ref
# dispatcher_codes to user modules via virtual mehtods 
# which do nothing in default implementation in baseClass.
# Those virtual methods are called from dispatcher method @ref
# dispatcher.dispatcher.dispatcher._handle_events which is called from @ref
# events.events.event.loop function. This function is called directly from main
# application thread. Events are registered from @ref
# hardware.serialHardware.Hardware._do_packet function which runs in dedicated
# thread for receiving data from serial channel. That is <b>receive
# direction</b> from wireless slave modules.
#
# <b>Transmit direction</b> to wireless slave modules behaves differently. User modules just use
# dispatcher method @ref dispatcher.dispatcher.dispatcher.send_packet which
# calls hardware method @ref hardware.serialHardware.Hardware.put_ack_payload.
# This method register sending request to a request queue. Requests are one by
# one processed and the queue is emptied step by step.
# 
