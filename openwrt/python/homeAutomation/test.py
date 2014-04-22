__author__ = 'kubanec'


import sys
from hardware import serialHardware
from events import events
import logging
from dispatcher import dispatcher


FORMAT = '%(levelname)s: \t %(asctime)s  %(name)s:%(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)

a = logging.getLogger("root")
a.setLevel(logging.WARN)

disp = dispatcher.dispatcher()
disp.start()

try:
    events.event.loop()
except KeyboardInterrupt:
    print "bye bye"

except:
    a.exception("application crashed")

