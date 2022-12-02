from flask import Blueprint
from classes.plugin import Plugin
from classes.browser import Firefox
from classes.net import NET
import re
import json
from utils.common import girc, base64encode
from hosts.streamlare import StreamLare

n2embed = Blueprint("2embed", __name__)

class toEmbed(Plugin):
    def __init__(self) -> None:
        self.metadata = {
            "name": "2embed",
            "desc": "Plugin for grabbing streams from 2embed.to",
            "author": "Parrot Developers",
            "id": "2embed",
            "logo": "logo.png",
            "resolver": {
                "name": "2embed",
                "ext": "mp4",
                "func": self.resolve,
            }
        }
    
    
    
    def resolve(self, imdbid, episode=None):
        url = f"https://www.2embed.to/embed/imdb/movie?id={imdbid}"
        if episode:
            episode = episode.split("-")
            season = episode[0]
            episode = episode[1]
            url = f"https://www.2embed.to/embed/imdb/tv?id={imdbid}&s={season}&e={episode}"

        firefox = Firefox()

        resp = NET().GET(url, headers=firefox.headers)
        dataID = re.findall(
            re.compile('data-id="(.*?)">Server Streamlare</a>', flags=re.MULTILINE), resp.text
        )[0]

        token = girc(
            resp.text,
            url,
            'aHR0cHM6Ly93d3cuMmVtYmVkLnRvOjQ0Mw..', # Decoded: https://2embed.to:443
            useNET=True
        )
        firefox.addHeader("Referer", url)
        embedurl = NET().GET(f"https://www.2embed.to/ajax/embed/play?id={dataID}&_token={token}", headers=firefox.headers).json()["link"]
        url, headers = StreamLare().grab(embedurl)
        return f"/api/proxy/base64:{base64encode(url)}&headers={base64encode(json.dumps(headers))}&token=[[token]]"

    # Required
    def blueprint(self) -> Blueprint:
        return n2embed
