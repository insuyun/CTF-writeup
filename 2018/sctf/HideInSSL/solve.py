from pypacker import ppcap
from pypacker.layer12 import ethernet
from pypacker.layer3 import ip
from pypacker.layer4 import tcp
import struct

def u32(x):
    return struct.unpack('<I', x)[0]

preader = ppcap.Reader(filename="HideInSSL.pcap")

npic = 0

data = {}
response = {}

keys = []
need_to_add = False

for ts, buf in preader:
    eth = ethernet.Ethernet(buf)
    try:
        if eth[ethernet.Ethernet, ip.IP, tcp.TCP] is not None:
            if eth[tcp.TCP].dport == 443 and eth.ip.dst_s == "192.168.0.128":
                for record in eth.ip.tcp.ssl.records:
                    if record.type == 22:
                        x = len("\x01\x00\x00\xab\x03\x03[\x1e\x7f\\")
                        body_len = len(eth.ip.tcp.ssl.records[0].body_bytes)
                        length = u32(record.body_bytes[x:x+4])
                        y = record.body_bytes[x+4:x+4+length]
                        port = eth[tcp.TCP].sport
                        response[port] = y

        if eth[tcp.TCP].sport == 443 and eth.ip.src_s == "192.168.0.128":
            port = eth[tcp.TCP].dport
            if eth.ip.tcp.body_bytes == b'1':
                if not port in data:
                    data[port] = b""
                    keys.append(port)
                data[port] += response[port]
    except AttributeError:
        pass

for i, k in enumerate(keys):
    d = data[k]
    with open("out/%d.jpg" % i, "wb") as f:
        f.write(d)

