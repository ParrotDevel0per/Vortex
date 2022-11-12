import re
import requests
from urllib.parse import urlparse
import base64
import json

class BeautifyM3U8:
    def __init__(self):
        self.patterns = {
            "url": r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            "m3u8ts": r"[\r\n]+^(?!#)^(?!http)((?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)",
        }

    def createProxifiedLink(self, proxyServer, url, headers):
        token = {
            "url": url,
            "headers": headers
        }
        token = base64.b64encode(json.dumps(token).encode('utf-8'))
        if ".ts" in url:
            return proxyServer + "chunk.ts?token=" + token.decode('utf-8')
        else:
            return proxyServer + "playlist.m3u8?token=" + token.decode('utf-8')



    def beautify(self, url, headers, proxyServer=None):
        response = requests.get(url, headers=headers)
        responseText = response.text
        parsed = urlparse(response.url)
        path = parsed.path
        filename = path .split("/")[-1]
        baseURL = response.url.split(filename)[0]
        domain = response.url.split(path)[0]

        # We need this to make all links look the same
        if "http" not in responseText or "#EXT-X-KEY:METHOD=AES-128" in responseText:
            matches = re.findall(self.patterns["m3u8ts"], responseText, re.MULTILINE)
            for match in matches:
                if not match.startswith("/"): responseText = responseText.replace(match, baseURL + match)
                else: responseText = responseText.replace(match, domain + match)
        
        matches = re.findall(self.patterns["url"], responseText, re.MULTILINE)
        for match in matches:
            responseText = responseText.replace(match, self.createProxifiedLink(proxyServer, match, headers))
        return responseText