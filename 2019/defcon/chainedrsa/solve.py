from pwn import *
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Util.number import *
import glob
import re

#context.log_level = 'DEBUG'

def read_privkeys():
    privkeys = {}
    for path in glob.glob('log/*.out'):
        name = os.path.basename(path)
        digest = name[:-4]
        key = open(os.path.join('data/%s/PUB') % digest).read()

        data = open(path).read()
        m = re.search('Found: .*, (.*)', data)
        if m:
            privkeys[key] = int(m.groups()[0], 10)
    return privkeys


privkeys = read_privkeys()
print('Found keys: %d' % len(privkeys))

flag = ""
answers = []

while True:
    try:
        trial = 0
        r = remote('chainedrsa.quals2019.oooverflow.io', 5000)

        seed = int(r.readline()[len('Seed: '):], 16)

        while True:
            pubkey = r.recvuntil('-----END PUBLIC KEY-----\n')

            pd, bit = r.readline()[6:].split(', ')
            pd = int(pd, 16)
            bit = int(bit, 10)

            digest = r.readline()[len('Digest: '):].strip()
            enc_msg = r.readline()[len('Encrypted Msg: '):].strip().decode('hex')

            if len(answers) > trial:
                msg = answers[trial]
            else:
                if pubkey in privkeys:
                    rsa_pub = RSA.importKey(pubkey)

                    d = privkeys[pubkey]
                    n, e = rsa_pub.n, rsa_pub.e

                    rsa_priv = RSA.construct((n, e, d, 0L, 0L, 0L))
                    cipher = PKCS1_v1_5.new(rsa_priv)

                    msg = ''
                    xor_msg = cipher.decrypt(enc_msg, 1)

                    hex_digest = digest.decode('hex')

                    for i, ch in enumerate(xor_msg):
                       msg += chr(ord(ch) ^ ord(hex_digest[i]))
                    answers.append(msg)
                    flag += msg.strip()[-1]
                    print('Flag: %s' % flag)

                else:
                    print('Failed to find a priv key for digest: %s' % digest)
                    time.sleep(1)
                    break

            print('%s: %s' % (trial, msg))
            r.sendline(msg)
            r.recvuntil('Yes, continue\n')
            trial += 1


    finally:
        r.close()

# flag: OOO{pr0f35510n4l_r54_br34k3r}
