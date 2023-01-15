import re
import base64
import binascii
import random
import string
import json
from classes.browser import Firefox
from utils.common import girc, get_hidden
from urllib.parse import urlparse
from classes.net import NET


class StreamSB:
    def __init__(self) -> None:
        pass

    def grab(self, url):
        parsed = urlparse(url)
        host = parsed.netloc
        media_id = parsed.path.split("/")[-1]
        web_url = f"https://{host}/d/{media_id}.html"
        rurl = 'https://{0}/'.format(host)
        headers = {'User-Agent': Firefox().ua,
                   'Referer': rurl}
        html = NET().get(web_url, headers=headers).text
        sources = re.findall(r'download_video([^"]+)[^\d]+(?:\d+x)?(\d+)', html, re.MULTILINE)

        if sources:
            sources.sort(key=lambda x: int(x[1]), reverse=True)
            sources = [(x[1] + 'p', x[0]) for x in sources]

            code, mode, dl_hash = eval(sources[0][1])

            dl_url = 'https://{0}/dl?op=download_orig&id={1}&mode={2}&hash={3}'.format(host, code, mode, dl_hash)
            html = NET().get(dl_url, headers=headers).text
            domain = base64.b64encode((rurl[:-1] + ':443').encode('utf-8')).decode('utf-8').replace('=', '')
            token = girc(html, rurl, domain)
            if token:
                payload = get_hidden(html)
                payload.update({'g-recaptcha-response': token})
                req = NET().post(dl_url, data=payload, headers=headers).text
                r = re.search('href="([^"]+).+?>(?:Direct|Download)', req)
                if r:
                    return r.group(1), headers

        eurl = self.get_embedurl(host, media_id)
        headers.update({'watchsb': 'sbstream'})
        html = NET().get(eurl, headers=headers).text
        data = json.loads(html).get("stream_data", {})
        strurl = data.get('file') or data.get('backup')
        if strurl:
            headers.pop('watchsb')
            return strurl, headers

        return "", {}

    def get_embedurl(self, host, media_id):
        # Copyright (c) 2019 vb6rocod
        def makeid(length):
            t = string.ascii_letters + string.digits
            return ''.join([random.choice(t) for _ in range(length)])

        x = '{0}||{1}||{2}||streamsb'.format(makeid(12), media_id, makeid(12))
        c1 = binascii.hexlify(x.encode('utf8')).decode('utf8')
        x = '{0}||{1}||{2}||streamsb'.format(makeid(12), makeid(12), makeid(12))
        c2 = binascii.hexlify(x.encode('utf8')).decode('utf8')
        x = '{0}||{1}||{2}||streamsb'.format(makeid(12), c2, makeid(12))
        c3 = binascii.hexlify(x.encode('utf8')).decode('utf8')
        return 'https://{0}/sources49/{1}/{2}'.format(host, c1, c3)
