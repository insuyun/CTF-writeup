#!/usr/bin/env python
from __future__ import print_function
import sys
import struct
import hashlib
import commands
import os

# inspired by C3CTF's POW

def pow_hash(challenge, solution):
    return hashlib.sha256(challenge.encode('ascii') + struct.pack('<Q', solution)).hexdigest()

def check_pow(challenge, n, solution):
    h = pow_hash(challenge, solution)
    return (int(h, 16) % (2**n)) == 0

def solve_pow(challenge, n):
    return int(commands.getoutput("%s %s %d"% (os.path.join(os.path.dirname(__file__), "pow"), challenge, n)))

    candidate = 0
    while True:
        if check_pow(challenge, n, candidate):
            return candidate
        candidate += 1

if __name__ == '__main__':
    challenge = sys.argv[1]
    n = int(sys.argv[2])

    print('Solving challenge: "{}", n: {}'.format(challenge, n))

    solution = solve_pow(challenge, n)
    print('Solution: {} -> {}'.format(solution, pow_hash(challenge, solution)))
