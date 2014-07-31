__author__ = 'kubanec'


import sys
from hardware import serialHardware
from events import events
import logging
import logging.handlers
from dispatcher import dispatcher
import time


#singleton
import fcntl
import os
pid_file = '/var/run/homeAutomation.pid'
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
cout = logging.StreamHandler()
cout.setFormatter(formater)
cout.setLevel(logging.WARN)



print "Zdravim jak svina, deme na to!"

a = logging.getLogger("root")
a.setLevel(logging.WARN)

a.addHandler(cout)
a.addHandler(fh)
a.addHandler(fh_error)

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

