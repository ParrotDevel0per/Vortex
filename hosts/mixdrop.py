from classes.browser import Firefox
from utils.unpacker import unpack
import re
from classes.net import NET

class MixDrop:
    def __init__(self):
        self.firefox = Firefox()

    def grab(self, url, referer):
        self.firefox.addHeader("Referer", "https://mixdrop.co/")
        if referer:
            self.firefox.addHeader("Referer", referer)
        html =  NET().get(url, headers=self.firefox.headers).text
        if not "(p,a,c,k,e,d)" in html: return None
        packed = "eval" + html.split("eval")[1].split(".split('|'),0,{}))")[0] + ".split('|'),0,{}))"
        unpacked = unpack(packed)
        pattern = r"wurl=\"(.*?)\""
        match = re.search(pattern, unpacked)
        if match:
            return "https:" + match.group(1), self.firefox.headers
        return None, None
