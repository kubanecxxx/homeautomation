'''
Created on 8. 9. 2015

@author: kuba
'''

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtNetwork

import viewer_ui
import pickle
import logging

class viewer(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self,parent)        
        self.ui = viewer_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.control_socket = QtNetwork.QTcpSocket()
        self.control_socket.readyRead.connect(self.control_socket_new_data)
        self.control_socket.disconnected.connect(self.control_disconnected)
        self.control_socket.connected.connect(self.control_connected)
        
        self.server = QtNetwork.QTcpServer()
        self.server.newConnection.connect(self.new_connection)
        
        
        self.ui.buttonOpen.clicked.connect(self.button_open)
        self.ui.buttonClose.clicked.connect(self.button_close)
        self.ui.buttonStart.clicked.connect(self.button_start)
        self.ui.buttonStop.clicked.connect(self.button_stop)
        self.ui.buttonShell.clicked.connect(self.button_shell)
        
        self.enable_panel(False)

    def enable_panel(self,en):
        self.ui.buttonClose.setEnabled(en)
        self.ui.buttonOpen.setDisabled(en)
        self.ui.buttonStart.setEnabled(en)
        self.ui.buttonStop.setEnabled(en)
        self.ui.spinControl.setDisabled(en)
        self.ui.editIP.setDisabled(en)
        
                    
    def new_connection(self):
        c = self.sender().nextPendingConnection()
        c.readyRead.connect(self.log_data)
        
    def log_data(self):
        socket = self.sender()
        st = socket.readAll()
        st = str(st)
        st = st[4:]
        p = pickle.loads(st)
        r =  logging.makeLogRecord(p)
        FORMAT = '%(asctime)s  [%(name)s]:[%(levelname)s] - %(message)s'
        formater= logging.Formatter(FORMAT)
        msg =  formater.format(r)
        self.ui.plainOutput.appendPlainText(QtCore.QString(msg))
    
    def control_connected(self):
        self.statusBar().showMessage("Connected",1000)
        self.enable_panel(True)
        pass
    
    def control_disconnected(self):
        self.statusBar().showMessage("Disconnected",1000)
        self.enable_panel(False)
        
    def control_socket_new_data(self):
        data = self.control_socket.readAll()
        self.ui.plainReturn.appendPlainText(str(data))
        pass
            
    def button_open(self):
        self.tcp_open(True)
        pass
    
    def button_close(self):
        self.tcp_open(False)
        pass
    
    def button_start(self):
        self.server.listen(port=self.ui.spinPort.value())
        st = "start %d\n" % self.ui.spinPort.value()
        self.ui.spinPort.setDisabled(True)
        self.control_socket.write(st)
        pass
    
    def button_stop(self):
        st = "stop\n"
        self.control_socket.write(st)
        self.ui.spinPort.setEnabled(True)
        self.server.close()
        pass
    
    def button_shell(self):
        st = "threads\n"
        self.control_socket.write(st)
        pass
    
    def tcp_open(self, opn):
        ok = False
        if opn:
            self.control_socket.connectToHost(self.ui.editIP.text(), self.ui.spinControl.value())
            ok = self.control_socket.isWritable()
        else:
            self.control_socket.close()
            
       
        pass