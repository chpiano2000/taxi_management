from PyQt5 import QtCore, QtGui
import sys, time
import socket
import re
ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1234

mess = ""

def updateMess(ms):
    mess = ms

class Outside(QtCore.QThread):
    update = QtCore.pyqtSignal(str)
    
    def __init__(self, parent, m, n):
        super(Outside, self).__init__(parent)
        self.m = m
        self.n = n
 
    def run(self):
        print('Waiting for connection')
        #try to connect
        try:
            ClientSocket.connect((host, port))
        except socket.error as e:
            print(str(e))

        Response = ClientSocket.recv(1024)
        global mess
        send = True
        
        while send:
            time.sleep(1)
            if(mess!=""):
                if(mess=="stop"):
                    ClientSocket.close()
                    break
                ClientSocket.sendall(str.encode(mess))
                mess=""
                
            else:
                ClientSocket.send(str.encode("heartbeat"))
                Response = ClientSocket.recv(1024)
                res = str(Response.decode('utf-8'))
                if(Response):
                    print("Got response "+ Response.decode('utf-8'))
                    if ((res!="ack") and (res!="ackack")):
                        
                        print(res[:3])
                        if res[:3] == 'ack':
                            res = res[3:]
                            
                        self.n = res
                        print(self.n)
                        self.update.emit(self.n)
            
            
    def stop(self):
        self.terminate()
      
