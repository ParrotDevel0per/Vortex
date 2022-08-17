import requests
import json
import string
import binascii
import random
from urllib.parse import urlparse

def get_embedurl(host, media_id):
    def makeid(length):
        t = string.ascii_letters + string.digits
        return ''.join([random.choice(t) for _ in range(length)])
    x = '{0}||{1}||{2}||streamsb'.format(makeid(12), media_id, makeid(12))
    c1 = binascii.hexlify(x.encode('utf8')).decode('utf8')
    x = '{0}||{1}||{2}||streamsb'.format(makeid(12), makeid(12), makeid(12))
    c2 = binascii.hexlify(x.encode('utf8')).decode('utf8')
    x = '{0}||{1}||{2}||streamsb'.format(makeid(12), c2, makeid(12))
    c3 = binascii.hexlify(x.encode('utf8')).decode('utf8')
    return 'https://{0}/sources43/{1}/{2}'.format(host, c1, c3)

def sbplay(url, referer=None):
    parsed = urlparse(url)
    host = parsed.netloc
    media_id = parsed.path.replace('/e/', '').replace("/", "")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    headers.update({'Referer': 'https://{0}/'.format(host)})
    if referer: headers.update({'Referer': referer})
    headers.update({'watchsb': 'streamsb'})
    html = requests.get(get_embedurl(host, media_id), headers=headers).text
    data = json.loads(html).get("stream_data", {})
    strurl = data.get('file') or data.get('backup')
    if strurl:
        headers.pop('watchsb')
        return strurl, headers
    return None, None