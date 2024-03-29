import os
import sys
from utils.paths import ADDONS_FOLDER


class Plugin:
    def __init__(self) -> None:
        self.css = {}
        self.blueprints = []
        self.sources = {}
        self.plugins = []
        self.access = {"public": [], "admin": []}
        self.setData()

    def __getSubclasses(self):
        return Plugin.__subclasses__()

    def setData(self):
        for klass in self.__getSubclasses():
            # Add all blueprints
            self.blueprints.append(klass().blueprint())

            metadata = klass().metadata
            self.plugins.append({
                "name": metadata["name"],
                "desc": metadata["desc"],
                "author": metadata["author"],
                "id": metadata["id"],
                "logo": metadata["logo"],
                "open": metadata["open"] if "open" in metadata else "",
                "settings": metadata["settings"] if "settings" in metadata else [],
                "addsCSS": "css" in metadata and metadata["css"],
                "addsSource": "source" in metadata and metadata["source"] != {}
            })

            # Add custom css
            if "css" in metadata and metadata["css"]:
                self.css.update(metadata["css"])
            
            # Check for sources
            if "source" in metadata and metadata["source"]:
                self.sources[metadata["source"]["name"]] = {
                    "run": metadata["source"]["func"],
                }

            if "admin" in metadata and metadata["admin"]:
                self.access["admin"].extend(metadata["admin"])

            if "public" in metadata and metadata["public"]:
                self.access["public"].extend(metadata["public"])
