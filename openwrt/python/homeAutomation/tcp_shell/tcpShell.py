'''
Created on 8. 9. 2015

@author: kuba
'''

import logging
import logging.handlers
import socket
import threading
import time
import select
import cmd
import errno

class tcpShell:
    def __init__(self, listening_port, main_logger_name):
        self._tcp = None
        self._thread = None
        self._var = threading.Event()
        self._var.set()
        self._log = logging.getLogger(main_logger_name + ".TCP_Shell")
        self._log.setLevel(logging.DEBUG)
        self._log.debug("tcp controller init")
        self._port = listening_port
        self._ml = logging.getLogger(main_logger_name)
        self._connections = []            
    
    def __del__(self):
        self._log.debug("destructor")
        self.clean()
        
    def clean(self):
        self._log.debug("Closing thread")
        self._var.clear()        
        for c in self._connections:
            c.clean()
        
        if self._thread.isAlive():
            self._thread.join()
        
    def start(self):
        TCP_PORT = self._port
        TCP_HOST = ""
        self.TCP_ADDR = (TCP_HOST,TCP_PORT)
        self._tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._tcp.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR, 1)
        self._tcp.bind(self.TCP_ADDR)
        self._tcp.listen(5)
        self._tcp.setblocking(False)
        self._tcp.settimeout(0.5)
        
        self._thread = threading.Thread(target=self._listening_thread, name="log controller thread")
        #self._thread.setDaemon(True)
        self._thread.start()
                
    def _listening_thread(self):
        self._log.info("waiting for connection on port %d" % self._port)
        while self._var.isSet():
            self._log.debug("active threads %d" % threading.activeCount())
            try:    
                time.sleep(1)
                self._list_thread()
         
            except socket.timeout:
                pass 
            except IOError,e:
                if e.errno != errno.EINTR:
                    raise
            except:
                self._log.exception("listening thread throws an exception:")
                pass
            
        self._log.info("Thread closed")
        self._tcp.shutdown(socket.SHUT_RDWR)
        self._tcp.close()
    
    def _list_thread(self):
        # check for new connections
        conn, addr = self._tcp.accept()
        self._log.debug("got a new connection " + str(conn) +str(" ")+  str(addr))   
        conn.setblocking(False)
        c = connection(self._ml,conn)
        self._connections.append(c)
                 
                    
class connection:
    counter = 0
    def __init__(self,main_logger,conn):
        self._buffer = ""
        self._handler = None
        self._ml = main_logger
        self._conn = conn
        self._number = connection.counter
        connection.counter += 1
        
        self._var = threading.Event()
        self._var.set()
        
        n = conn.getpeername()
        p = n[1]
        n = n[0]
        name = self._ml.name
        self._log = logging.getLogger("%s.tcp_shell %s:%d" % (name,n,p))                
        self._thread = threading.Thread(target=self._socket_thread, name=("log_socket %s:%d thread" % (n,p)))
        self._thread.setDaemon(True)
        self._thread.start()
        self._cleaned = False
                        
    def clean(self):
        if self._cleaned:
            return
        self._cleaned = True
        self._log.info("cleaning up")
        self._var.clear()
        if self._handler:
            self._ml.handlers.remove(self._handler)
                                    
        try:                        
            self._conn.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self._conn.close()
        
        #wait for thread termination
        if threading.currentThread() != self._thread:
            self._thread.join()
        self._log.info("succesfully cleaned up")
        
    def _socket_thread(self):
        self._log.info("socket thread started")
        while self._var.isSet():
            try:
                ok = self._serve_connection()
                if not ok:
                    self._log.info("connection has been closed")
                    self.clean()
                    
                time.sleep(0.5)                                                 
            except:
                pass            
            
        self._log.info("socket thread finished")
        
    def __del__(self):
        self._log.debug("destructor")
        self.clean()
            
    def _serve_connection(self):
        conn = self._conn
        data = self._buffer
        try:
            read,write,error = select.select([conn,],[conn,],[conn,],0)
        except :
            return False
                            
        if (len(read) > 0):     
            read = conn.recv(64)
            ## check if connection is still alive
            if (len(read) == 0):
                return False
                     
            data+= read      
            
            #handle data
            dic = {}            
            b = data.split("\n")         
            
            for a in b:                
                a = a.strip()
                if (len (a) == 0):
                    continue
                f = a.find(" ")
                 
                if f == -1:
                    cmd = a
                    val = ""
                else:
                    cmd = a[0:f]
                    val = a[f:]                                
                dic[cmd] = val
            
            if "\n" in data:
                a = data.rindex("\n")                            
                data = data[a+1:]
           
            if len(dic):
                self._shell(dic)
                pass
        
        self._buffer = data
        return True
    
    def _shell(self,dic):
        conn = self._conn
        hn = self._handler
        
        #start on port        
        if dic.has_key("start"):
            try:
                port = int(dic["start"])
                addr =  conn.getpeername()[0]
                hn = logging.handlers.SocketHandler(addr, port)
                hn.setLevel(1)
                hn.makeSocket()
                self._ml.addHandler(hn)                                                
                self._handler = hn 
                conn.send("Ready port %d" % port)                                   
            except:
                conn.send("Cannot open port")
                self._log.exception("Cannot start logging to port")
                
        if dic.has_key("stop"):
            try:
                if (hn):
                    conn.send("Removed")
                    self._ml.handlers.remove(hn)
                    hn.close()
                    self._handler = None                
            except:
                self._log.exception("cannot remove handler by stop command")
        
        if dic.has_key("threads"):
            try:
                i = 0
                for thd in threading.enumerate():
                    i += 1
                    conn.send("%d - %s \n" %(i,str(thd)))                
            except:
                pass
        
            