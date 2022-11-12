from ..utils.browser import Firefox
from ..utils.resolve import Resolver
import requests
import re
from utils.unpacker import unpack
from bs4 import BeautifulSoup
import string

class Gomo(Resolver):
    def __init__(self):
        self.firefox = Firefox()
        self.useALT = False

    def getParts(self, url):
        html = requests.get(url, headers=self.firefox.headers).text
        try:
            tc = re.findall(r"var tc = '(.*?)';", html)[0]
        except:
            raise Exception(html)
        _token = html.replace("\n", "").split("_token\": \"")[1].split("\",")[0]
        sliceF = re.search(r"slice\((.*?)\)", html).group(1)
        matches = re.search(r"\) \+ \"(.*?)\"\+\"(.*?)\";", html)
        return tc, _token, matches, sliceF

    def fuckToken(self, token, matches, slices):
        slices = slices.split(",")
        return token[int(slices[0]):int(slices[1])][::-1] + str(eval(matches.group(1) + matches.group(2)))

    def getSources(self, url):
        tc, _token, matches, slices = self.getParts(url)
        headers = self.firefox.headers
        headers.update({"x-token": self.fuckToken(tc, matches, slices)})
        data = {"tokenCode": tc, "_token": _token}
        resp = requests.post("https://gomo.to/decoding_v3.php", headers=headers, data=data, allow_redirects=True)
        sources = eval(resp.text.replace('\/', '/'))
        return list(set([source for source in sources if "gomo" in source]))

    def gomo(self, url):
        headers = self.firefox.headers.copy()
        sources = self.getSources(url)
        if self.useALT:
            url = [source for source in sources if "vid1" in source][0]
            resp = requests.get(url).text
            mirrorServer = "http:" + re.search(r'<a href="(.*?)"><li>Mirror Server</li></a>', resp).group(1)
            resp = requests.get(mirrorServer).text
        
        packages = []
        for src in sources:
            try:
                resp = requests.get(src, headers=headers).text
                soup = BeautifulSoup(resp, features="lxml")
                for item in soup.find_all('script'):
                    innerHTML = item.encode_contents().decode("utf-8")
                    if '(p,a,c,k,e,d)' in innerHTML:
                        packages.append(innerHTML)
            except Exception as e:
                pass
        

        unpacked = unpack(packages[0])
        print(unpacked)
        if requests.get(unpacked.split("$.get('")[1].split("'")[0] + "1").text != "1": print("", end="") #print("Error might occur")
        unpacked = unpacked.split("[")[1].split("]")[0]
        try:
            m3u8Source = f'http{re.search(r"http(.*?)m3u8", unpacked).group(1)}m3u8'
            return m3u8Source
        except Exception as e: pass
        try:
            mp4Sources = [f'http{source}mp4' for source in re.findall(r"http(.*?)mp4", unpacked.replace(m3u8Source, ""))]
        except Exception as e:
            mp4Sources = [f'http{source}mp4' for source in re.findall(r"http(.*?)mp4", unpacked)]
        labelsDef = re.findall(r'label:"(.*?)"', unpacked)
        labels = []
        for label in labelsDef:
            if len(label) == 6:
                firstPart = label[:3]
                secondPart = label[3:]
                labels.append(f"{firstPart}x{secondPart}")
            else: labels.append(label)
        return mp4Sources[0]

    def grab(self, imdbid, episode):
        url = f"https://gomo.to/movie/{imdbid}"
        if episode:
            episode = episode.split("-")
            season = episode[0]
            episode = episode[1]
            if episode in string.digits[1:]: episode = "0" + episode
            if season  in string.digits[1:]: season = "0" + season
            url = f"https://gomo.to/show/{imdbid}/{season}-{episode}"

        return {
            "url": self.gomo(url),
            "headers": self.firefox.headers
        }
