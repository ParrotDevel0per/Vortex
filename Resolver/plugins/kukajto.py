from ..utils.browser import Firefox
from ..utils.resolve import Resolver
import requests
import re
from bs4 import BeautifulSoup
import requests
from cloudscraper import CloudScraper
from bs4 import BeautifulSoup
from ..utils.common import translateItemToCzech
import base64
import re
import difflib
import ResolveURL


class KukajTo(Resolver):
    def __init__(self):
        self.firefox = Firefox()

    def search(self, query):
        headers = self.firefox.headers
        headers.update({"Referer": "https://kukaj.io/"})
        return requests.get(f"https://kukaj.io/search/json?q={query.replace(' ', '+')}", headers=headers).json()

    def kukajto(self, url):
        headers = self.firefox.headers.copy()
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

    def grab(self, imdbid, episode):
        isMovie = episode is None
        translatedTitle = translateItemToCzech(imdbid, isMovie)
        results = self.search(translatedTitle)
        data = {
            "titles": [],
            "slugs": [],
        }
        for result in results:
            if isMovie and result['t'] == 'movie':
                data['titles'].append(result['name'])
                data['slugs'].append(result['slug'])
            elif not isMovie and result['t'] == 'show':
                data['titles'].append(result['name'])
                data['slugs'].append(result['slug'])
        if len(data['titles']) == 0: return "No results found"
        bestMatch = difflib.get_close_matches(translatedTitle, data['titles'], n=1, cutoff=0.5)[0]
        index = data['titles'].index(bestMatch)
        id = data['slugs'][index]
        url = f"https://film.kukaj.io/{id}"
        if not isMovie:
            episode = episode.split("-")
            season = episode[0]
            episode = episode[1]
            if len(episode) == 1: episode = "0" + episode
            if len(season) == 1: season = "0" + season
            url = f"https://serial.kukaj.io/{id}/S{season}E{episode}"
        resolved = self.kukajto(url)
        headers = None
        if "mixdrop" in resolved:
            resolved, headers = ResolveURL.resolve("MixDrop", resolved, "https://kukaj.io/")
            headers["Referer"] = "https://mixdrop.co/"
        else:
            resolved, headers = ResolveURL.resolve("StreamTape", resolved, "https://kukaj.io/")

        return {
            "url": resolved,
            "headers": headers
        }