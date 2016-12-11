import sys
import hashlib
C = "LMIG}RPEDOEEWKJIQIWKJWMNDTSR}TFVUFWYOCBAJBQ"
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ{}"
mapping = """A|ABCDEFGHIJKLMNOPQRSTUVWXYZ{}
B|BCDEFGHIJKLMNOPQRSTUVWXYZ{}A
C|CDEFGHIJKLMNOPQRSTUVWXYZ{}AB
D|DEFGHIJKLMNOPQRSTUVWXYZ{}ABC
E|EFGHIJKLMNOPQRSTUVWXYZ{}ABCD
F|FGHIJKLMNOPQRSTUVWXYZ{}ABCDE
G|GHIJKLMNOPQRSTUVWXYZ{}ABCDEF
H|HIJKLMNOPQRSTUVWXYZ{}ABCDEFG
I|IJKLMNOPQRSTUVWXYZ{}ABCDEFGH
J|JKLMNOPQRSTUVWXYZ{}ABCDEFGHI
K|KLMNOPQRSTUVWXYZ{}ABCDEFGHIJ
L|LMNOPQRSTUVWXYZ{}ABCDEFGHIJK
M|MNOPQRSTUVWXYZ{}ABCDEFGHIJKL
N|NOPQRSTUVWXYZ{}ABCDEFGHIJKLM
O|OPQRSTUVWXYZ{}ABCDEFGHIJKLMN
P|PQRSTUVWXYZ{}ABCDEFGHIJKLMNO
Q|QRSTUVWXYZ{}ABCDEFGHIJKLMNOP
R|RSTUVWXYZ{}ABCDEFGHIJKLMNOPQ
S|STUVWXYZ{}ABCDEFGHIJKLMNOPQR
T|TUVWXYZ{}ABCDEFGHIJKLMNOPQRS
U|UVWXYZ{}ABCDEFGHIJKLMNOPQRST
V|VWXYZ{}ABCDEFGHIJKLMNOPQRSTU
W|WXYZ{}ABCDEFGHIJKLMNOPQRSTUV
X|XYZ{}ABCDEFGHIJKLMNOPQRSTUVW
Y|YZ{}ABCDEFGHIJKLMNOPQRSTUVWX
Z|Z{}ABCDEFGHIJKLMNOPQRSTUVWXY
{|{}ABCDEFGHIJKLMNOPQRSTUVWXYZ
}|}ABCDEFGHIJKLMNOPQRSTUVWXYZ{""".splitlines()
d = {}

for m in mapping:
    k, v = m.split("|")
    d[k] = v

p = "SECCON{"
k = ""
c = "LMIG}RPEDOEEWKJIQIWKJWMNDTSR}TFVUFWYOCBAJBQ"
for i in xrange(len(p)):
    pidx = chars.index(p[i])
    cidx = chars.index(c[i])
    k += (chars[(cidx - pidx) % len(chars)])

for a1 in chars:
    for a2 in chars:
        for a3 in chars:
            for a4 in chars:
                for a5 in chars:
                    k1 = k + a1 + a2 + a3 + a4 + a5
                    p1 = ""

                    k1 = "VIGENERECODE"
                    for i in xrange(len(c)):
                        cidx = chars.index(c[i])
                        kidx = chars.index(k1[i % len(k1)])
                        ch = chars[(cidx - kidx) % len(chars)]
                        p1 += ch
                    print(p1)
                    h = hashlib.md5(p1).hexdigest()
                    if h == "f528a6ab914c1ecf856a1d93103948fe":
                        print("FOUND! : %s" % k1)
                        sys.exit(-1)
