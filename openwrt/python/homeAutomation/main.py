
__author__ = 'kubanec'


import sys
from hardware import serialHardware
from events import events
import logging
import logging.handlers
from dispatcher import dispatcher
import time
import logger.controller

#singleton
import fcntl
import os
#pid_file = '/var/run/homeAutomation.pid'
pid_file = '/tmp/homeautom.pid'
fp = open(pid_file, 'w')
try:
    fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    fp.write(str(os.getpid()))
    fp.write("\n\r")
    fp.flush()
except IOError:
    print "another instance is running"    
    sys.exit(1)


# setup logging facility
FORMAT = '%(asctime)s  [%(name)s]:[%(levelname)s] - %(message)s'
#logging.basicConfig(format=FORMAT)
formater= logging.Formatter(FORMAT)

import inspect, os
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory

fh = logging.handlers.RotatingFileHandler(path + "/log.txt",maxBytes=(1024*1024*5),backupCount=7)
fh_error = logging.handlers.RotatingFileHandler(path + "/errors.txt",maxBytes=(1024*1024*5),backupCount=7)
fh.setFormatter(formater)
fh.setLevel(logging.WARN)
fh_error.setFormatter(formater)
fh_error.setLevel(logging.ERROR)
cout = logging.StreamHandler(sys.stdout)
cout.setFormatter(formater)
cout.setLevel(logging.DEBUG)

stderr = logging.StreamHandler(sys.stderr)
stderr.setLevel(logging.WARN)

print "How are you doing everybody let's start "

a = logging.getLogger("root")
a.addHandler(stderr)
a.setLevel(logging.DEBUG)

logging.getLogger("root.apps").addHandler(cout)

#a.addHandler(cout)
a.addHandler(fh)
a.addHandler(fh_error)

jaja = logger.controller.loggerSetup()

a.warn("application started")

# start the application 
disp = dispatcher.dispatcher()
disp.start()

try:
    events.event.loop()
except KeyboardInterrupt:
    a.warn("application disabled by CTRL+C")
    print "bye bye"

except:
    a.exception("application crashed")


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
