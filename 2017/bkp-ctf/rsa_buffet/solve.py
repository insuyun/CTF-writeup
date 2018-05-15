from Crypto.Cipher import AES,PKCS1_OAEP
from Crypto.PublicKey import RSA
from base64 import b64decode
import encrypt
from secretsharing import PlaintextToHexSecretSharer as SS

values = [0, 4, 3, 6]
plains = [[], [], [], []]
for i in values:
    with open("pkey-%d.pem" % i) as f:
        data = f.read()
    data = data.splitlines()
    data = data[1:-1]
    data = ''.join(data)

    keyDER = b64decode(data)
    keyPriv = RSA.importKey(keyDER)

    for j in xrange(1, 6):
        with open("ciphertext-%d.bin" % j, 'rb') as f:
            data = f.read()
        data = encrypt.decrypt(keyPriv, data)
        if data is not None:
            values = data.splitlines()[1:]
            for i, v in enumerate(values):
                plains[i].append(v)
for v in plains:
    print(SS.recover_secret(v))

