import os
from utils.paths import ADDONS_FOLDER

class Plugin:
    def __init__(self) -> None:
        self.css = {}
        self.blueprints = []
        self.resolvers = {}
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
                "addsCSS": "css" in metadata and metadata["css"],
                "addsResolver": "resolver" in metadata and metadata["resolver"] != {}
            })

            # Add custom css
            if "css" in metadata and metadata["css"]:
                self.css.update(metadata["css"])
            
            # Check for resolvers
            if "resolver" in metadata and metadata["resolver"]:
                self.resolvers[metadata["resolver"]["name"]] = {
                    "run": metadata["resolver"]["func"],
                    "ext": metadata["resolver"]["ext"]
                }

            if "admin" in metadata and metadata["admin"]:
                self.access["admin"].extend(metadata["admin"])

            if "public" in metadata and metadata["public"]:
                self.access["public"].extend(metadata["public"])

# Import all addons
for addon in os.listdir(ADDONS_FOLDER):
    if os.path.isdir(os.path.join(ADDONS_FOLDER, addon)):
        continue

    if addon.startswith("__"):
        continue

    exec(open(os.path.join(ADDONS_FOLDER, addon, "addon.py"), "r", encoding="utf-8").read())

# Import preinstalled addons
for addon in os.listdir(os.path.join(os.getcwd(), "addons")):
    if os.path.isdir(os.path.join(os.getcwd(), "addons", addon)) == False:
        continue

    if addon.startswith("__"):
        continue


    exec(open(os.path.join(os.getcwd(), "addons", addon, "addon.py"), "r", encoding="utf-8").read())
