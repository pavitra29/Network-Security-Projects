import socket
import sys
import json
import base64
import time

#creating socket
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error,msg:
	print 'Error is ' + str(msg[0])
	sys.exit()
#connecting the socket
s.connect(("localhost",2002))
print 'Socket connected'

# sending data to service 

# JSON request to send {command: "AUTH",user: tractableambush}
try:
	s.sendall('{"command":"AU')
	print 'command 1 sent'
	time.sleep(1)
	print 'waiting for 1 seconds'
	s.sendall('TH","user":"tractableambush"}')
	print 'command 2 sent'

except socket.error:
	print 'Send failed'
	sys.exit()

# receiving reply from server
try:
reply = s.recv(1000)
print reply
except socket.error:
	print 'receive failed'
	sys.exit()

# closing the socket 
s.close()
