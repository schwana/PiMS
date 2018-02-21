import socket
import time
import struct
import re
#import unidecode

TCP_IP='192.168.0.3'
TCP_PORT = 818
BUFFER_SIZE=4
MESSAGE='ID? \r'

SCAN='MR40 \r'

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

s.send('\r')

time.sleep(0.1)
print (s.recv(1024))
s.send('Admin\r')
print(s.recv(1024))
time.sleep(0.1)
s.send('admin\r')
print(s.recv(1024))
time.sleep(0.1)

print("Scan Starting")
s.send(SCAN)
time.sleep(1)
hex_string = s.recv(BUFFER_SIZE)

u=struct.unpack('<i',hex_string)[0]
uf=u*1e-16
s.close()

print("u: ", uf)

fo = open("/home/pi/PiMS/DisplaySRS/M40.txt", "r")
line = fo.readline()
fo.close()

fo = open("/home/pi/PiMS/DisplaySRS/M40.txt", "w")
fo.write(str(uf))
fo.close()



