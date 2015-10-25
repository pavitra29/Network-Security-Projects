import base64
import socket
import random, base64
from hashlib import sha1
import sys
import json
import struct
from collections import OrderedDict
from Crypto.Cipher import ARC4 as cipher

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 5452
s.connect(('127.0.0.1', port))
data = open('data.json').read()

print "NEEDHAM SCHROEDER"

json_len = len(data)
ascii_json = chr(json_len)
json_4byte = "\0\0\0"+str(ascii_json)

s.send(json_4byte)
s.send(data)

key = '\xeb\xb0\x18\xbd\xa2\x09\xde\xbb\xc4\x5e\x77\x00\xdc\x0e\x99\xb5'

l=struct.unpack('>I',s.recv(4))[0]
result=s.recv(l)
result_len=len(result)

s.close

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host=socket.gethostname()
port=5453
s.connect(('127.0.0.1',port))
obj=cipher.new(key)
json_reply=json.loads(obj.encrypt(result))

blob=json_reply["blob"]
session_key=json_reply["session_key"]

blob=base64.b64decode(blob)
session_key=base64.b64decode(session_key)

s.sendall(struct.pack('>I',len(blob)))
s.sendall(blob)

bob_4byte=s.recv(4)
bob=s.recv(176)

obj=cipher.new(session_key)
bob_reply=json.loads(obj.decrypt(bob))

nonce=bob_reply["nonce"]
nonce_minus_1 = nonce - 1

nonce_encrypt=obj.encrypt(json.dumps({'nonce':nonce_minus_1}))
s.sendall(struct.pack('>I',len(nonce_encrypt)))
s.sendall(nonce_encrypt)

secret_4byte=struct.unpack('>I',s.recv(4))[0]
secret=s.recv(secret_4byte)

print "FIRST SECRET", json.loads(obj.encrypt(secret))

s.close

print "REPLAY ATTACK"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 5453
s.connect(('127.0.0.1', port))
data = open('data.json').read()

stolen_key = open('stolen_key').read()

blob = open('blob_replay').read()

s.sendall(struct.pack('>I',len(blob)))
s.sendall(blob)

bob_4byte=s.recv(4)
bob=s.recv(176)

obj=cipher.new(stolen_key)
bob_reply=json.loads(obj.decrypt(bob))

nonce=bob_reply["nonce"]
nonce_minus_1 = nonce - 1

nonce_encrypt=obj.encrypt(json.dumps({'nonce':nonce_minus_1}))
s.sendall(struct.pack('>I',len(nonce_encrypt)))
s.sendall(nonce_encrypt)

secret_4byte=struct.unpack('>I',s.recv(4))[0]
secret=s.recv(secret_4byte)

print "SECOND SECRET", json.loads(obj.encrypt(secret))

s.close
