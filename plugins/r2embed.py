import requests
import re

def grab(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    resp = requests.get(url, headers=headers).text
    hlsURL = re.findall(r"<source src=\"(.*?)\" ", resp)
    return url.split("/play/")[0] + "/play/" + hlsURL[0], headers