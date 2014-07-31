'''
Created on 9. 7. 2014

@author: kubanec
'''
from threading import Thread, Event, Timer
import time            
            
def TimerReset(*args, **kwargs):
    """ Global function for Timer """
    return _TimerReset(*args, **kwargs)


class _TimerReset(Thread):
    """Call a function after a specified number of seconds:

    t = TimerReset(30.0, f, args=[], kwargs={})
    t.start()
    t.cancel() # stop the timer's action if it's still waiting
    """

    def __init__(self, interval, function, args=[], kwargs={}):
        Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.stop = Event()
        self.now = time.time()

    def cancel(self):
        """Stop the timer if it hasn't finished yet"""
        self.stop.set()

    def run(self):
       # print "Time: %s - timer running..." % time.asctime()
        
        self.now = time.time()
        while not self.stop.isSet():
            self.stop.wait(self.interval)
            if (self.now + self.interval < time.time()):
                break
        else:
            return
        
        #print "function called"
        self.function(*self.args, **self.kwargs)
        

    def reset(self, interval=None):
        """ Reset the timer """
        if interval:
            self.interval = interval
        
        #print "timer reset"
        self.now = time.time()
        

