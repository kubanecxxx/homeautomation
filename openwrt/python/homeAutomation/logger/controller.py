'''
Created on 24. 1. 2015

@author: kubanec
'''

import logging
import socket
import threading
import time
import errno
import logging.handlers
import config

class loggerSetup:
    def __init__(self):
        self._tcp = None
        self._thread = None
        self._var = threading.Event()
        self._var.set()
        self._log = logging.getLogger("root.loggerController")
        self._log.setLevel(logging.DEBUG)
        self.tcp_init()
        self._log.debug("tcp controller init")
        pass
    
    def add_handler(self, logger_name, level, ip, port):
        pass
    
    def tcp_init(self):
        TCP_PORT = config.config_dict["logging_control_port"]
        TCP_HOST = ""
        self.TCP_ADDR = (TCP_HOST,TCP_PORT)
        self._tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._tcp.bind(self.TCP_ADDR)
        self._tcp.listen(5)
        self._thread = threading.Thread(target=self._listening_thread, name="log controller thread")
        self._thread.setDaemon(True)
        self._thread.start()
    
    def terminate_thread(self):
        self._var.clear()
    
    def _listening_thread(self):
        try:
            self._list_thread()
        except:
            pass
        
    def _list_thread(self):
        while self._var.isSet():
            self._log.debug("thread waiting for connection")
            conn, addr = self._tcp.accept()
            self._log.debug("got connection " + str(conn) +str(" ")+  str(addr))
            thd = threading.Thread(target = self._socket_thread,args= (conn,addr), name = "socket thread " + str(addr))
            thd.setDaemon(True)
            thd.start()
            
        self._log.info("thread terminated")
        self._tcp.close()
        
    def _socket_thread(self, conn, addr):
        '@type conn: socket.socket'
        var = threading.Event()
        var.set()
        hn = handlers(addr[0],conn)
        
        try:
            while var.isSet():    
                data = conn.recv(128)    
                #check if the connecion is closed from the other end
                if (data == ""):
                    var.clear()
                    hn._clear_handlers()
                    continue
                
                hn._process_data(data)
        except:
            pass
        conn.close()
        self._log.debug("socket thread terminated " + str(addr))
        pass
    
    
#addlogger:root.app.neco,port:55899,level:0-50,end
class handlers:
    def __init__(self,addr,conn):
        '@type conn: socket.socket'
        self._data = ""
        self._addr = addr
        self._conn = conn
        self.lst = []
        pass
    
    def _parse(self):
        end = self._data.find("end")
        if end != -1:
            msg = self._data[0:end+3]
            self._data = self._data[end + 3:]
            return msg
            
        return False
    
    def _do_msg(self,msg):
        '@type msg: str'
        ja = msg.split(",")
        ja = ja[0:-1]
        map = {}
        for a in ja:
            t = a.split(":")
            map[t[0]] = t[1]
        
        command = map.keys()[0]
        if command == "addlogger":
            logg = map["addlogger"]
            port = int(map["port"])
            level = int(map["level"])
            self._add_handler(logg, port, level)
        elif command == "getloggers":
            lg = self._get_loggers().keys()
            self._send(lg,"loggers")
        elif command == "getHandlers":
            lg = map["getHandlers"]
            hn = logging.getLogger(lg).handlers
            self._send(hn,"handlers")
        elif command == "setlevel":
            logger = map["setlevel"]
            handler = map["handlerIdx"] #index
            level = map["level"]
            lg = logging.getLogger(logger)
            try:
                lg.handlers[handler].setLevel(level)
            except:
                pass         
        elif command == "deleteHandler":
            logger = map["deleteHandler"]
            handler = map["handlerIdx"] #index
            lg = logging.getLogger(logger)
            try:
                h = lg.handlers[handler]
                lg.handlers.remove(h)
            except:
                pass
        
    def _process_data(self,data):
        self._data += data
        msg = self._parse()
        if msg:
            try:
                self._do_msg(msg)
            except Exception, e:
                print e
                
        
        pass
    
    def _clear_handlers(self):
        "@type log: logging.Logger"
        print self.lst
        for a in self.lst:
            log,sh = a
            log.removeHandler(sh)
            
        self.lst =[]
        pass
    
    
    def _add_handler(self,logger,port,level):
        try:
            sh = logging.handlers.SocketHandler(self._addr,port)
            sh.setLevel(level)
            log = logging.getLogger(logger)
            self.lst.append((log,sh))
            log.addHandler(sh)
            sh.makeSocket()
                        
        except Exception, e:
            print e
            
        
    def _get_loggers(self):
        ja = logging.Logger.manager.loggerDict
        return ja
        
    def _send(self,lst,name):
        st = name + ","
        for a in lst:
            st += a
            st += ","
        st += "end"
        self._conn.send(st)
        