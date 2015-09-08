##
# @defgroup Events
# @brief simple event system
# @{

import Queue
import pickle
import time
import logging
import threading

##
# @brief Event class 
# constains simple api for registering callbacks which 
# are called in @ref loop() method which is called in application 
# main thread
#
# all methods are static - there is no need to instanciate class 
# and register method can be used in whole application
class event:
    _queue = Queue.Queue()
    _evt = threading.Event()
    _evt.set()

    def __init__(self):
        pass
    
    ##
    # @brief this method is called in main thread and proccess
    # the registered callbacks in queue
    @staticmethod
    def loop():
        #process callbacks from queue
        while event._evt.isSet():
            time.sleep(0.1)
            if not event._queue.empty():
                cb = event._queue.get()
                f = cb[0]
                f(pickle.loads(cb[1]))
        pass
    
    ##
    # @brief register method to the processing queue
    # @param callback function or method to be called in main thread
    # the callback function has to accept one argument
    # @param args this argument is passed to the callback
    @staticmethod
    def register_event(callback, args):
        t = (callback,pickle.dumps(args))
        event._queue.put(t)
        pass
    
    ##
    # @brief if this method is called event loop will end
    @staticmethod
    def register_exit(code = 1):
        event._evt.clear()
        if code == 1:
            n = threading.current_thread().name
            logging.getLogger("root").exception("thread \"%s\" caused exception, application terminated",n)        
    
##
# @}
