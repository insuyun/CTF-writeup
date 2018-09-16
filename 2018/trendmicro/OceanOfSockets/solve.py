import string

key = "%|r%uL5bbA0F?5bC0E9b0_4b2?N"

g1 = []
g2 = []
ans = ""
for j in xrange(len(key)):
    g1.append(chr((ord(key[j]) + 47) % 256))
    g2.append(chr((ord(key[j]) - 47) % 256))

    if g1[-1]  in string.printable:
        ans += g1[-1]
    else:
        ans += g2[-1]

print(ans)
