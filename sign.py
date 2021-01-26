import hashlib, requests, time, random

serverTimeUrl = 'https://www.ximalaya.com/revision/time'
headers = {'user-agent': 'ximalaya/0.0.1'}
hashStrPrefix = 'himalaya-'
signTemplate = '%s(%d)%s(%d)%d'

def getSign():
    sign = ''
    res = requests.get(serverTimeUrl, headers=headers)
    if res.status_code == 200 and res.headers['content-type'] == 'text/plain; charset=utf-8':
        timeStr = res.text
        clientTime = round(time.time() * 1000)
        hashStr = hashStrPrefix + timeStr
        rand1 = random.randint(1, 99)
        rand2 = random.randint(1, 99)
        sign = signTemplate%(hashlib.md5(hashStr.encode('utf-8')).hexdigest(), rand1, timeStr, rand2, clientTime)
        print('sign: ', sign)
    return sign 