from flask import Blueprint
from classes.plugin import Plugin

name = "vidsrc"
vidsrcBP = Blueprint(name, __name__)


class VidSrc(Plugin):
    def __init__(self) -> None:
        self.metadata = {
            "name": "VidSrc",
            "desc": "Adds an vidsrc.me embed",
            "author": "Parrot Developers",
            "id": "vidsrc",
            "logo": "logo.png",
            "source": {
                "name": "vidsrc",
                "func": self.grab,
            }
        }


    def grab(self, imdbid, episode=None):
        url = "https://v2.vidsrc.me/embed/{}/".format(imdbid)
        if episode != None: url += "{}/".format(episode)
        return url

    # Required
    def blueprint(self) -> Blueprint:
        return vidsrcBP
