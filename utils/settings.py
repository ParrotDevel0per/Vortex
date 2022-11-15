from cryptography.fernet import Fernet
from utils.paths import DB_FOLDER
import os
import json

default = {
    "ip": "127.0.0.1",
    "port": "5000",
    "cachePosters": "True",
    "source": "gomo",
    "proxifyM3UPosters": "True",
    #"preloader": "1.png",
    "language": "en",
    "debug": "false",
    "fernetKey": str(Fernet.generate_key()).replace("b'", "").replace("'", ""),
    "keepLogs": "False"
}

def setToDefault():
    open(SETTINGSFILE, 'w').write(json.dumps(default))

SETTINGSFILE = os.path.join(DB_FOLDER, "settings.json")
if not os.path.exists(SETTINGSFILE): setToDefault()
settingsKeys = [
    "ip",
    "port",
    "cachePosters",
    "source",
    "proxifyM3UPosters",
    #"preloader",
    "language",
    "debug",
    "fernetKey",
    "keepLogs"
]

for key in settingsKeys:
    settings = json.load(open(SETTINGSFILE, 'r'))
    if key not in settings:
        settings[key] = default[key]
        open(SETTINGSFILE, 'w').write(json.dumps(settings))


def getSetting(key):
    if key in settingsKeys:
        with open(SETTINGSFILE, 'r') as f:
            settings = json.load(f)
            return settings[key]
    else:
        return "Invalid Key"

def setSetting(key, value):
    if key in settingsKeys:
        with open(SETTINGSFILE, 'r') as f:
            settings = json.load(f)
            settings[key] = value
            open(SETTINGSFILE, 'w').write(json.dumps(settings))
            return f"{key.capitalize()} is now {value}"
    else:
        return "Invalid key"



