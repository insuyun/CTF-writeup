from pwn import *
from hashlib import md5

context.log_level = 'debug'

def sxor(s1, s2):
    s = ""
    for i in xrange(len(s1)):
        s += chr(ord(s1[i]) ^ ord(s2[i]))
    return s

BS = 16

r = remote('202.120.7.217',8221)
r.recvuntil('[l]ogin\n')
r.send("r\n")

name = "admin".ljust(16, "A") + "\x1b" * 16
r.send(name + "\n")

r.recvuntil("Here is your secret:\n")
h = r.readline().strip().decode("hex")

md5_before = md5(name + "\x10" * 16).digest()
md5_new = md5(name).digest()

new_iv = sxor(sxor(md5_before, md5_new), h[:BS])
new_h = new_iv + h[BS:-BS]
print(new_h.encode("hex"))

r.send("l\n")
r.send(new_h.encode("hex")+"\n")

r.interactive()

# flag{Easy_br0ken_scheme_cann0t_keep_y0ur_integrity}

