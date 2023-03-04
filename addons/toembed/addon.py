from flask import Blueprint
from classes.plugin import Plugin


n2embed = Blueprint("n2embed", __name__)

class toEmbed(Plugin):
    def __init__(self) -> None:
        self.metadata = {
            "name": "2embed",
            "desc": "Adds an 2embed embed",
            "author": "Parrot Developers",
            "id": "toembed",
            "logo": "logo.png",
            "source": {
                "name": "toembed",
                "func": self.grab,
            },
        }
    
    def grab(self, imdbid, episode=None):
        url = f"https://www.2embed.to/embed/imdb/movie?id={imdbid}"
        if episode:
            episode = episode.split("-")
            season = episode[0]
            episode = episode[1]
            url = f"https://www.2embed.to/embed/imdb/tv?id={imdbid}&s={season}&e={episode}"
        return url


    # Required
    def blueprint(self) -> Blueprint:
        return n2embed