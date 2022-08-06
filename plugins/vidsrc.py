import requests
from bs4 import BeautifulSoup
import re

def grab(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
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
    return hlsurl, path, src

def resolve(baseURL, id):
    url = f"{baseURL}/proxy/vidsrc/play?item={id}"
    return baseURL + requests.get(url).text