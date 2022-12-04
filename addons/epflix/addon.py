from flask import Blueprint
from classes.plugin import Plugin
from classes.browser import Firefox
from classes.net import NET
import re
import json
from utils.common import base64encode
from utils.unpacker import unpack
from urllib.parse import unquote

epflix = Blueprint("epflix", __name__)

class ePFlix(Plugin):
    def __init__(self) -> None:
        self.metadata = {
            "name": "ePFlix",
            "desc": "Plugin for grabbing streams from pflix.co",
            "author": "Parrot Developers",
            "id": "epflix",
            "logo": "logo.png",
            "resolver": {
                "name": "epflix",
                "func": self.resolve,
            }
        }
    
    
    
    def resolve(self, imdbid, episode=None):
        url = f"https://embed.pflix.co/movie-imdb.php?imdb={imdbid}"
        if episode:
            episode = episode.split("-")
            season = episode[0]
            episode = episode[1]
            url = f"https://embed.pflix.co/tv-imdb.php?imdb=[{imdbid}&s={season}&e={episode}"


        print(url)
        firefox = Firefox()

        resp = NET().GET(url, headers=firefox.headers)
        quoted = re.findall(r"document.write\(unescape\(\"(.*?)\"\)", resp.text, re.MULTILINE)[0].replace('</script>', '').replace('<script type="text/javascript">', '')
        source = re.findall(r'"file":"(.*?)"', unpack(unquote(quoted)), re.MULTILINE)[0]

        return f"/api/proxy/base64:{base64encode(source)}&headers={base64encode(json.dumps(firefox.headers))}&token=[[token]]"

    # Required
    def blueprint(self) -> Blueprint:
        return epflix
