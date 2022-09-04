import requests
from cloudscraper import CloudScraper
from bs4 import BeautifulSoup
import base64
import re
from utils.fakeBrowser import baseHeaders

def search(query):
    headers = baseHeaders
    headers.update({"Referer": "https://kukaj.io/"})
    return requests.get(f"https://kukaj.io/search/json?q={query.replace(' ', '+')}", headers=headers).json()

def grab(url):
    headers = baseHeaders
    scraper = CloudScraper()
    scraper.headers.update(headers)
    cookies = scraper.get(url).cookies.get_dict()
    html = requests.get(url, cookies=cookies, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')

    options = soup.find('div', {'class': 'col-md-12 subplayermenumob'}).find('select').find_all('option')
    opts = []
    embedUrl = ""
    for i in options:
        try:
            if i.text == "MIX":
                opts.append("MIX")
            if i.text == "TAP":
                opts.append("TAP")

        except:
            pass
    opts.sort()
    opt = opts[0] # For now, only one option is available
    for i in options:
        if i.text == opt:
             embedUrl = i.get('data-href')
    urlm = f"{url.split('.io/')[0]}.io{embedUrl}"
    scraper = CloudScraper()
    scraper.headers.update(headers)
    cookies = scraper.get(urlm).cookies.get_dict()
    html = requests.get(urlm, cookies=cookies, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    datakuk = soup.find('iframe', {'id': 'kukframe'}).get('data-kuk')
    datakuk = base64.b64decode(datakuk).decode('utf-8').split('":"')[1].split('","')[0].replace('\/', '/')
    datakuk = base64.b64decode(datakuk).decode('utf-8')
    headers.update({'Referer': url})
    scraper = CloudScraper()
    scraper.headers.update(headers)
    cookies = scraper.get(datakuk).cookies.get_dict()
    html = requests.get(datakuk, cookies=cookies, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    iframes = soup.find_all('iframe')
    embedSources = []
    for i in iframes:
        if i.get('data-kk'):
            embedSources.append(i.get('data-kk'))
    embedSources.sort(key=len, reverse=True)
    embedSource = embedSources[0]
    embedSource = base64.b64decode(embedSource).decode("utf-8")
    subtitleUrls = [f"https://kukaj.io/subtitles/v2/{i}.vtt" for i in re.findall(r'https://kukaj.io/subtitles/v2/(.*?).vtt', embedSource)]
    return embedSource
