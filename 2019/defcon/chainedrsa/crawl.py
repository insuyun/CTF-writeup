from pwn import *
from Crypto.PublicKey import RSA

from multiprocessing import Pool


s = set()

while True:
    r = remote('chainedrsa.quals2019.oooverflow.io', 5000)
    dirp = "data"

    if not os.path.exists(dirp):
        os.mkdir(dirp)

    seed = int(r.readline()[len('Seed: '):], 16)
    pubkey = r.recvuntil('-----END PUBLIC KEY-----\n')

    pd, bit = r.readline()[6:].split(', ')
    pd = int(pd, 16)
    bit = int(bit, 10)

    digest = r.readline()[len('Digest: '):].strip()
    enc_msg = int(r.readline()[len('Encrypted Msg: '):], 16)

    if not digest in s:
        os.mkdir('%s/%s' % (dirp, digest))
        open('%s/%s/DIGEST' % (dirp, digest), 'w').write(digest)
        open('%s/%s/PUB' % (dirp, digest), 'w').write(pubkey)
        open('%s/%s/PD' % (dirp, digest), 'w').write(str(pd))
        open('%s/%s/BIT' % (dirp, digest), 'w').write(str(bit))
        open('%s/%s/ENC' % (dirp, digest), 'w').write(str(enc_msg))
        s.add(digest)
        print('add %s' % digest)

    r.close()
