from utils.unpacker import unpack
import requests
import re

def mixdrop(url, referer=None):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    headers.update({'Referer': 'https://mixdrop.co/'})
    if referer: headers.update({'Referer': referer})
    html = requests.get(url, headers=headers).text
    if not "(p,a,c,k,e,d)" in html: return None
    packed = "eval" + html.split("eval")[1].split(".split('|'),0,{}))")[0] + ".split('|'),0,{}))"
    unpacked = unpack(packed)
    pattern = r"wurl=\"(.*?)\""
    match = re.search(pattern, unpacked)
    if match: return "https:" + match.group(1), headers
    return None, None