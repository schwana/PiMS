import socket
import time

TCP_IP='192.168.0.3'
TCP_PORT= 818

FIL_ON='ID?\r'

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

s.send('/r')

#time.sleep(5)

print (s.recv(1024))

time.sleep(2)
#Username
s.send('Admin\r')
print (s.recv(1024))
time.sleep(2)
#Password
s.send('admin\r')
print (s.recv(1024))
time.sleep(2)
print (s.recv(1024))

print('Turn on filament')

s.send(FIL_ON)
time.sleep(5)
print (s.recv(1024))

s.close()
