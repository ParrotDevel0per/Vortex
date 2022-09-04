import requests
from bs4 import BeautifulSoup
from utils.fakeBrowser import baseHeaders
import re

def grab(url):
    headers = baseHeaders
    headers.update({"Referer": "https://vidsrc.me/",})
    s = requests.session()
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    iframe = soup.find('iframe', id='player_iframe')
    src = iframe['src'].replace('//', 'https://')
    headers.update({'Referer': src})
    r = s.get(src, headers=headers)
    src = re.search(r'src: \'(.*?)\'', r.text).group(1).replace("//", "https://")
    headers.update({'Referer': src})
    r = s.get(src, headers=headers)
    hlsurl = re.search(r'video.setAttribute\("src" , "(.*?)"\)', r.text).group(1)
    path = re.findall(r'var path = "(.*?)"', r.text)[1].replace("//", "https://")
    hdrs = baseHeaders
    hdrs["Referer"] = "https://vidsrc.stream/"
    return hlsurl, path, hdrs
