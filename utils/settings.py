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
    "keepLogs": "False",
    "saveIPs": "False"
}

# https://stackoverflow.com/questions/34327719/get-keys-from-json-in-python
def get_simple_keys(data):
    result = []
    for key in data.keys():
        if type(data[key]) != dict:
            result.append(key)
        else:
            result += get_simple_keys(data[key])
    return result

def setToDefault():
    open(SETTINGSFILE, 'w').write(json.dumps(default))

SETTINGSFILE = os.path.join(DB_FOLDER, "settings.json")
if not os.path.exists(SETTINGSFILE): setToDefault()
settingsKeys = get_simple_keys(default)

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



