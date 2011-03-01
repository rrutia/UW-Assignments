#!/usr/bin/python
import socket

HOST = 'localhost'    # The remote host
PORT = 50014              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send('1')
s.send('1')

data = s.recv(1024)
s.close()
print 'Received', repr(data)





