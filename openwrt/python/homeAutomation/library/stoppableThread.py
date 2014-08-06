'''
Created on 5. 8. 2014

@author: kubanec
'''

import threading

class stoppableThread(threading.Thread):
    def __init__(self,**kwds):
        super(stoppableThread,self).__init__(**kwds)
        self._stop = threading.Event()
    def stop(self):
        self._stop.set()
    def stopped(self):
        return self._stop.isSet()