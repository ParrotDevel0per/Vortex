import re
import requests

def streamtape(web_url, referer=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'Referer': referer
    }
    r = requests.get(web_url, headers=headers).text
    src = re.findall(r'''ById\('.+?=\s*(["']//[^;<]+)''', r)
    if src:
        src_url = ''
        parts = src[-1].replace("'", '"').split('+')
        for part in parts:
            p1 = re.findall(r'"([^"]*)', part)[0]
            p2 = 0
            if 'substring' in part:
                subs = re.findall(r'substring\((\d+)', part)
                for sub in subs:
                    p2 += int(sub)
            src_url += p1[p2:]
        src_url += '&stream=1'
        src_url = 'https:' + src_url if src_url.startswith('//') else src_url
        return src_url, headers
    return None, None
