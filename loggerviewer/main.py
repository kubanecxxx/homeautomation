'''
Created on 24. 1. 2015

@author: kubanec
'''

import time
import socket
import viewer
from PyQt4 import QtGui
import sys

def bdak():
    soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    soc.connect(("localhost",5555))
    soc.send("addlogger:root.moje,")
    time.sleep(0.1)
    soc.send("port:6868,")
    time.sleep(0.1)
    soc.send("level:0,endaddlogger")
    

    try:
        while True:
            time.sleep(0.1)
            d = soc.recv(32)
            if (d == ""):
                print "Connection Closed"
                break
    except KeyboardInterrupt:
        print "Ctrl + C pressed"
             
    
    soc.close()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    #w = logger.superLogger()
    w = viewer.viewer()
    w.show()
    
    app.exec_()
    pass
