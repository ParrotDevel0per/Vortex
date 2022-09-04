import requests
from bs4 import BeautifulSoup
from utils.fakeBrowser import baseHeaders

def getCurrentVidembedURL():
    return requests.get("https://vidembed.io", headers=baseHeaders, allow_redirects=False).headers["Location"]

def resolveVidembed(vidembedURL, server):
    html = requests.get(vidembedURL, headers=baseHeaders).text
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('li', {'class': 'linkserver', 'data-status': '1'})
    names, urls = [], []
    for link in links:
        names.append(link.text)
        urls.append(link['data-video'])
    if len(urls) == 1: return urls[0]
    index = names.index(server)
    return urls[index]