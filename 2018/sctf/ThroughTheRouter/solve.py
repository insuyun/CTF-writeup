from scapy.all import *

r = Raw(load='secret')
a=IP(dst='10.0.0.1', src='10.1.7.8')/UDP(dport=22136, sport=5555)/r
print(str(a).encode("hex"))
print(repr(str(a)))
