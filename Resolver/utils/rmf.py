import requests
from urllib.parse import urlencode

class ResolvedMediaFile:
    def __init__(self, url, headers, refresher={}):
        self.url = url
        self.hlsurl = self.url
        self.headers = headers
        self.refresher = refresher

    def test(self):
        resp = requests.get(self.url, headers=self.headers)
        if resp.status_code in range(200, 400):
            return True

        if "m3u" in resp.text.lower():
            return True

        return False

    def urlencoded(self):
        return self.url + "|" + urlencode(self.headers)