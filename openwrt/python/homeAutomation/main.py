
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
cout = logging.StreamHandler(sys.stderr)
cout.setFormatter(formater)
cout.setLevel(logging.WARN)



print "Zdravim jak svina, deme na to!"

a = logging.getLogger("root")
a.setLevel(logging.DEBUG)

a.addHandler(cout)
a.addHandler(fh)
a.addHandler(fh_error)

jaja = logger.controller.loggerSetup()

a.warn("application started")

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
# @todo dot with colaboration
# @dot
# digraph jouda {
# node[shape=record]
# hw[label="Hardware" URL = "@ref hardware"]
# } 
# @enddot
# 
# user modules inherits from base class
# those modules are called from dispatcher method which is called from event
# loop -main thread; the events are registered from hardware module - receive
# direction; transmit direction user modules call dispatcher function for
# sending a data to wireless slaves this function calls hardware method which
# register this request to the sending queue which is one by one processed and
# emptied
# line between hardware and dispatcher is dispatcher codes set
# hardware uses serial codes for himself
# line between dispatcher communicate with user modules (base class) via
# dispatcher codes 
# base class distributes wireless data to user modules via @ref command_table codes
# nothing else then simple dictionary with integers and methods 
# dispatcher datas are directly passed to the user modules via _vmt
