import requests
from bs4 import BeautifulSoup

def getCurrentVidembedURL():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    return requests.get("https://vidembed.io", headers=headers, allow_redirects=False).headers["Location"]

def resolveVidembed(vidembedURL, server):
    html = requests.get(vidembedURL).text
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('li', {'class': 'linkserver', 'data-status': '1'})
    names, urls = [], []
    for link in links:
        names.append(link.text)
        urls.append(link['data-video'])
    if len(urls) == 1: return urls[0]
    index = names.index(server)
    return urls[index]