import base64
from Crypto.Util.number import getPrime, isPrime, getRandomNumber
 
KEY = int("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX".encode("hex"), 16)
 
def generate_key(n):
       p = getPrime(n)
       q = p
       while True:
               q += getRandomNumber(n/3)
               if (isPrime(q)):
                       break
       return (p,q)
 
(p,q) = generate_key(1024)
n = p * q
enc = pow(KEY, 65537, n)
print "n : %d" % n
print "enc : %s" % base64.b64encode(hex(enc)[2:-1].decode("hex"))
