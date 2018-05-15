from bs4 import BeautifulSoup

import requests

f = open("useragent.txt", "w")

for i in xrange(1, 468):
    print("CRAWL %d" % i)
    url = 'https://developers.whatismybrowser.com/useragents/explore/software_name/firefox/%d' % i
    r  = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)

    for link in soup.find_all('a'):
        if "useragents" in link.get('href'):
            try:
                if "Mozilla" in link.string:
                    f.write(link.string + "\n")
            except UnicodeEncodeError:
                pass
    r.close()
