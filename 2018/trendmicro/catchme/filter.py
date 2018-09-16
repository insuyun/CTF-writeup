import ipaddress
ips = set(open('ip.txt').read().strip().split(","))
rules = open("filter.txt").read().strip().split(",")

all_matched = []

for rule in rules:
    matched = []
    n = ipaddress.ip_network(rule)
    netw = int(n.network_address)
    mask = int(n.netmask)

    for ip in ips:
        a = int(ipaddress.ip_address(ip))
        in_network = (a & mask) == netw
        if in_network:
            matched.append(ip)
    if matched:
        print(rule, matched)
        all_matched.extend(matched)
        print("ips: %d, matched: %d" % (len(ips), len(all_matched)))

print(set(ips) - set(all_matched))
