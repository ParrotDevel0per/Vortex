from ..utils.browser import Firefox
from ..utils.resolve import Resolver
import requests
import re
from bs4 import BeautifulSoup

class Vidsrc(Resolver):
    def __init__(self):
        self.firefox = Firefox()

    def vidsrc(self, url):
        self.firefox.addHeader("Referer", "https://vidsrc.me/")
        s = requests.session()
        r = s.get(url, headers=self.firefox.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        iframe = soup.find('iframe', id='player_iframe')
        src = iframe['src'].replace('//', 'https://')
        self.firefox.addHeader("Referer", src)
        r = s.get(src, headers=self.firefox.headers)
        src = re.search(r'src: \'(.*?)\'', r.text).group(1).replace("//", "https://")
        self.firefox.addHeader("Referer", src)
        r = s.get(src, headers=self.firefox.headers)
        hlsurl = re.search(r'video.setAttribute\("src" , "(.*?)"\)', r.text).group(1)
        path = re.findall(r'var path = "(.*?)"', r.text)[1].replace("//", "https://")
        self.firefox.reInitHeaders()
        self.firefox.addHeader("Referer", "https://vidsrc.stream/")
        return hlsurl, path, self.firefox.headers

    def grab(self, imdbid, episode):
        url = "https://vidsrc.me/embed/{}/".format(imdbid)
        if episode != None: url += "{}/".format(episode)
        hlsurl, refresher, headers = self.vidsrc(url)

        return {
            "url": hlsurl,
            "headers": headers,
            "refresher": {
                "url": refresher,
                "headers": headers
            }
        }