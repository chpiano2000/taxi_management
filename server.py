import socket
import os
from _thread import *
import threading

#Server configuration
ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1234
ThreadCount = 0

#Try to start the socket
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(500)

lock = threading.Lock()
gMsg = ""


def threaded_client(connection):
    connection.send(str.encode('You are connected'))
    global gMsg
    msg = gMsg
    try:
        while True:
            
            lock.acquire()
            
            if (msg!=gMsg): 
                msg=gMsg
                connection.sendall(str.encode(msg))
                print(msg)
            else:
                connection.sendall(str.encode("ack"))
            
            lock.release()
            
            data = connection.recv(2048)
            reply = data.decode('utf-8')
        
            if (data and (reply!="heartbeat")):
                print(reply)
                lock.acquire()
                gMsg = reply
                lock.release()
    except:
        print("One connection died of error")
        connection.close()
    connection.close()

while True:
    try:
        Client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(threaded_client, (Client, ))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    except:
        print("error")
ServerSocket.close()
