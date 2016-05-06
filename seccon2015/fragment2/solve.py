#!/usr/bin/python
import hpack
if __name__ == '__main__':
    data = ''
    with open('./fragment2.pcap', 'rb') as f:
        data = f.read()

    idx = data.find("\x00\x02\x06\x2a") + 4
    data = data[idx:]

    for i in xrange(len(data)):
        for j in xrange(i, len(data)):
            try:
                d = hpack.Decoder()
                print("DECODED : %s" % d.decode(data[i:j]))
            except Exception as e:
                print(e)
