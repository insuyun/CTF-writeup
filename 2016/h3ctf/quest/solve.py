import requests
import re
import base64
import zlib

url = 'http://10.10.10.29/quest'
logs = set()
def get_item(data = None):
    r = requests.post(url, data = data)
    m = re.search('name="info" value="(.*)"', r.text)

    for line in r.text.splitlines():
        if line.startswith('var items='):
            items = re.findall('"(.*?)"', line)
        if line.startswith('<div id="log">'):
            if not line in logs:
                print(line)
                logs.add(line)
    if m:
        return m.group(1), items

"""
visited = set()
info, items = get_item()
queue = []
queue.append((info, items))
while queue:
    info, items = queue.pop()
    items = []
    for i in xrange(15):
        items.append("item%02d" % i)
    visited.add(info)
    for item in items:
        data = {'info':info, 'click':"%s:0" % item}
        new_info, new_items = get_item(data)
        #print(new_info, new_items)
        if not new_info in visited:
            queue.append((new_info, new_items))
"""
print("TRY NEW")
info = "eJyrVsrMK0vNK8kvqlSyUog21VEwiNVRUCrOLEkF8o2AzKLU3PwyECfaHCSTn5ZWnFoC5BrUAgAufhHH"
info = base64.b64decode(info)
print(zlib.decompress(info))
print(base64.b64encode(zlib.compress('{"inventory": [5, 6, 0], "site": 2, "remove": [7], "offset": 0}')))
