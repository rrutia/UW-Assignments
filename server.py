#!/usr/bin/python
import socket

HOST = ''        # Symbolic name meaning all available interfaces
PORT = 50014              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr

while 1:
    input = conn.recv(1024)
    print input
    i = input
    i = int(i)
    num = i
    print sum(num)

    if not data: break
    conn.send(data)

conn.close()

