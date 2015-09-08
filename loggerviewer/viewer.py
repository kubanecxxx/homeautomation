'''
Created on 8. 9. 2015

@author: kuba
'''

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtNetwork
from PyQt4 import Qt

import viewer_ui
import pickle
import logging
import re
import struct
import ConfigParser


class viewer(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self,parent)        
        self.ui = viewer_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.control_socket = QtNetwork.QTcpSocket(self)
        self.control_socket.readyRead.connect(self.control_socket_new_data)
        self.control_socket.disconnected.connect(self.control_disconnected)
        self.control_socket.connected.connect(self.control_connected)
        
        self.server = QtNetwork.QTcpServer(self)
        self.server.newConnection.connect(self.new_connection)
        
        
        self.ui.buttonOpen.clicked.connect(self.button_open)
        self.ui.buttonClose.clicked.connect(self.button_close)
        self.ui.buttonStart.clicked.connect(self.button_start)
        self.ui.buttonStop.clicked.connect(self.button_stop)
        self.ui.editShell.returnPressed.connect(self.shell)
        
        self.enable_panel(False)
        
        self.buffer = []
        self.pointer = -1
        
        self.controlP = QtGui.QShortcut("Ctrl+P",self)
        self.controlP.activated.connect(self.controlP_cb)
        
        self.controlN = QtGui.QShortcut("Ctrl+N",self)
        self.controlN.activated.connect(self.controlN_cb)
        
        self.controlP = QtGui.QShortcut("Ctrl+O",self)
        self.controlP.activated.connect(self.button_open)
        
        self.controlP = QtGui.QShortcut("Ctrl+L",self)
        self.controlP.activated.connect(self.ui.editShell.setFocus)
        
        self.controlP = QtGui.QShortcut("Ctrl+J",self)
        self.controlP.activated.connect(self.shell)
        
        self.ui.editFilter.setText("root.*>8")
        self.buf = ""
        self.rest = 0
        
        
        try:
            self.read_file()
        except:
            print "no config file"
            pass
    
    def save_file(self):
        config = ConfigParser.RawConfigParser()
        config.add_section("setup")
        config.set("setup","controlPort",self.ui.spinControl.value())
        config.set("setup","logPort",self.ui.spinPort.value())
        config.set("setup","IP",self.ui.editIP.text())
        config.set("setup","filter",self.ui.editFilter.text())
        
        config.set("setup","geometry",self.saveGeometry().data())
        config.set("setup","state",self.saveState().data())
        
        
        with open('viewer.cfg', 'wb') as configfile:
            config.write(configfile)

    def read_file(self):
        config = ConfigParser.RawConfigParser()
        config.read("viewer.cfg")
        self.ui.spinControl.setValue(config.getint("setup", "controlPort"))
        self.ui.spinPort.setValue(config.getint("setup", "logPort"))
        self.ui.editIP.setText(config.get("setup", "IP"))
        self.ui.editFilter.setText(config.get("setup", "filter"))
        self.restoreGeometry(config.get("setup","geometry"))
        self.restoreState(config.get("setup","state"))
        
    def closeEvent(self, *args, **kwargs):
        self.save_file()
        return QtGui.QMainWindow.closeEvent(self, *args, **kwargs)
        
    def __del__(self):
        self.tcp_open(False)

    def enable_panel(self,en):
        self.ui.buttonClose.setEnabled(en)
        self.ui.buttonOpen.setDisabled(en)
        self.ui.buttonStart.setEnabled(en)
        self.ui.buttonStop.setEnabled(en)
        self.ui.spinControl.setDisabled(en)
        self.ui.editIP.setDisabled(en)
        
    def controlP_cb(self):
        if self.pointer > -1:
            self.ui.editShell.setText(self.buffer[self.pointer])
            self.pointer -= 1
        
    def controlN_cb(self):
        if self.pointer < len(self.buffer)-1:
            self.pointer += 1
            self.ui.editShell.setText(self.buffer[self.pointer])
            
        
    def new_connection(self):
        c = self.sender().nextPendingConnection()
        c.readyRead.connect(self.log_data)
        
     
    def _unpickle(self,socket):
        if self.rest == 0:
            size = socket.read(4)
            slen = struct.unpack(">L",size)[0]
            self.buf += socket.read(slen)
        
        if (len(self.buf) < slen):
            print "bdak"
            self.rest = slen - len(self.buf)
            return None
        
        p = pickle.loads(self.buf)
        self.buf = ""
        r =  logging.makeLogRecord(p)
        return r

    def _filter(self,msg):
        #import autoload
        exp = str(self.ui.editFilter.text())
        log = True
        
        name2 = msg.name
        level = msg.levelno    
        
        sp = exp.split("|")    
        dct = {}
                    
        if len(exp) > 0:
            log = False
            for a in sp:
                a = a.strip()
                b= a.split(">")
                name = str(b[0].strip())
                lev = int(b[1].strip())
                dct[name]= lev
            
            
            for n,lev in dct.iteritems():
                try:
                    sel = re.search(n,name2).group(0)    
                    l = sel == str(name2)                    
                    l2 = lev <= level
                    log =l and l2
                    
                    if log:
                        return True
                except:                
                    pass
                
                
        return log
            

    def log_data(self):
        socket = self.sender()
        i = 0
        while socket.bytesAvailable():                        
            r = self._unpickle(socket)
            if not r:
                return
              
            log = self._filter(r)

            if (log):
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
    
    def shell(self):
        st = self.ui.editShell.text() 
        self.control_socket.write((st + "\n").toLocal8Bit())
        self.buffer.append(st)
        self.pointer = len(self.buffer)-1
        self.ui.editShell.clear()
        pass
    
    def tcp_open(self, opn):
        ok = False
        if opn:
            self.control_socket.connectToHost(self.ui.editIP.text(), self.ui.spinControl.value())
            ok = self.control_socket.isWritable()
        else:
            self.control_socket.close()
            
       
        pass