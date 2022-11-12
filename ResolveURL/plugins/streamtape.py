from ..utils.browser import Firefox
from ..utils.resolve import Resolver
import requests
import re

class StreamTape(Resolver):
    def __init__(self):
        self.firefox = Firefox()

    def grab(self, web_url, referer=None):
        if referer:
            self.firefox.addHeader("Referer", referer)
        r = requests.get(web_url, headers=self.firefox.headers).text
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
            return src_url, self.firefox.headers
        return None, None
