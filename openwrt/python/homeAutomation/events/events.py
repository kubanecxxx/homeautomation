'''
Created on 28. 3. 2014

@author: kubanec
'''

import Queue
import pickle
import time
import logging
import threading

class event:
    _queue = Queue.Queue()
    _exit = True

    def __init__(self):
        pass
    
    @staticmethod
    def loop():
        #process callbacks from queue
        j = event._exit
        while j:
            time.sleep(0.1)
            if not event._queue.empty():
                cb = event._queue.get()
                f = cb[0]
                f(pickle.loads(cb[1]))
            j = event._exit
        pass
    
    @staticmethod
    def register_event(callback, args):
        t = (callback,pickle.dumps(args))
        event._queue.put(t)
        pass
    
    @staticmethod
    def register_exit():
        event._exit = False
        n = threading.current_thread().name
        logging.getLogger("root").exception("thread \"%s\" caused exception, application terminated",n)
        pass
    
