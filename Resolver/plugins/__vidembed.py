from ..utils.browser import Firefox
from ..utils.resolve import Resolver
import requests
import ResolveURL
import re
from bs4 import BeautifulSoup

class Vidembed(Resolver):
    def __init__(self):
        self.firefox = Firefox()

    def getCurrentVidembedURL(self):
        return requests.get("https://vidembed.io", headers=self.firefox.headers, allow_redirects=False).headers["Location"]

    def resolveVidembed(self, vidembedURL, server):
        html = requests.get(vidembedURL, headers=self.firefox.headers).text
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('li', {'class': 'linkserver', 'data-status': '1'})
        names, urls = [], []
        for link in links:
            names.append(link.text)
            urls.append(link['data-video'])
        if len(urls) == 1: return urls[0]
        index = names.index(server)
        return urls[index]

    def resolveGDrivePlayer(self, url):
        html = requests.get(url, headers=self.firefox.headers).text
        pattern = r"<a href=\"(.*?)\"><li>Mirror Server</li></a>"
        match = re.search(pattern, html)
        if match: return self.getCurrentVidembedURL() + match.group(1).split("/")[-1]
        return None

    def grab(self, imdbid, episode):
        url = f"https://database.gdriveplayer.us/player.php?imdb={imdbid}"
        if episode:
            episode = episode.split("-")
            url = f"https://series.databasegdriveplayer.co/player.php?type=series&imdb={imdbid}&season={episode[0]}&episode={episode[1]}"
        
        streamSBURL = self.resolveVidembed(self.resolveGDrivePlayer(url),'StreamSB').split("?")[0]
        resolved, headers = ResolveURL.resolve("SBPlay", streamSBURL)
        return {
            "url": resolved,
            "headers": headers
        }