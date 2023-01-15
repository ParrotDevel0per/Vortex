import re
from classes.browser import Firefox
from urllib.parse import urlparse
import cloudscraper
import time


class DoodStream:
    def __init__(self) -> None:
        pass

    def grab(self, web_url):
        firefox = Firefox()
        firefox.addHeader("Referer", "https://dood.wf/")
        parsed = urlparse(web_url)
        html = ""
        while not html:
            try:
                scraper = cloudscraper.create_scraper()
                html = scraper.get(web_url, headers=firefox.headers).text
            except:
                pass

        md5URL = "https://" + parsed.netloc + "/pass_md5/" + re.findall(r"'/pass_md5/(.*?)'", html, re.MULTILINE)[0]
        
        i = 0
        while i < 25:
            try:
                video = scraper.get(md5URL, headers=firefox.headers).text
                return  f"{video}?token={md5URL.split('/')[-1]}&expiry={int(time.time())}".strip(), firefox.headers
            except:
                i += 1
        return "", {}
