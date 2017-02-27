from mpc import *
import requests
import json

(n,g), (lam,mu) = paillier_keygen()

print(n ,g, lam, mu)

data = {}
data['n'] = n
data['g'] = g
data['poly'] = [1]
#r = requests.post('http://localhost:8080', json.dumps(data))
r = requests.post('http://54.191.171.202:1025', json.dumps(data))

data = json.loads(r.text)
answer = ""
for c in data:
    answer += chr(paillier_decrypt((n, g), (lam, mu), c) & 0xff)

print(repr(answer))
