from classes.browser import Firefox
from ..utils.resolve import Resolver
from ..utils.common import girc
from ..hosts.streamlare import StreamLare
import re
from classes.net import NET

class N2Embed(Resolver):
    def __init__(self):
        self.firefox = Firefox()
        self.source = "Streamlare"

    def n2embed(self, url):
        resp = NET().GET(url, headers=self.firefox.headers)
        dataID = re.findall(
            re.compile(f'data-id="(.*?)">Server {self.source}</a>', flags=re.MULTILINE), resp.text
        )[0]

        token = girc(
            NET().GET(url).text,
            url,
            'aHR0cHM6Ly93d3cuMmVtYmVkLnRvOjQ0Mw..', # Decoded: https://2embed.to:443
            useNET=True
        )
        print(token)

        self.firefox.addHeader("Referer", url)
        return NET().GET(f"https://www.2embed.to/ajax/embed/play?id={dataID}&_token={token}", headers=self.firefox.headers).json()["link"]

    def grab(self, imdbid, episode):
        url = f"https://www.2embed.to/embed/imdb/movie?id={imdbid}"
        if episode:
            episode = episode.split("-")
            season = episode[0]
            episode = episode[1]
            url = f"https://www.2embed.to/embed/imdb/tv?id={imdbid}&s={season}&e={episode}"
        resolved, headers = StreamLare().grab(self.n2embed(url))
        print(resolved)
        return {
            "url": resolved,
            "headers": headers
        }

