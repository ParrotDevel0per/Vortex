from utils.paths import DB_FOLDER
import os
import json
import typer

app = typer.Typer()

default = {
    "ip": "127.0.0.1",
    "port": "5000",
    "debug": "False",
    "adminPassword": "admin",
    "cachePosters": "True",
    "source": "gomo",
    "proxifyM3UPosters": "True",
    "checkForUpdates": "True",
    "preloader": "1.png"
}

def setToDefault():
    open(SETTINGSFILE, 'w').write(json.dumps(default))

SETTINGSFILE = os.path.join(DB_FOLDER, "settings.json")
if not os.path.exists(SETTINGSFILE): setToDefault()
settingsKeys = [
    "ip",
    "port",
    "debug",
    "adminPassword",
    "cachePosters",
    "source",
    "proxifyM3UPosters",
    "checkForUpdates",
    "preloader"
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
        return None

def setSetting(key, value):
    if key in settingsKeys:
        with open(SETTINGSFILE, 'r') as f:
            settings = json.load(f)
            settings[key] = value
            open(SETTINGSFILE, 'w').write(json.dumps(settings))
            return True
    else:
        return False

@app.command()
def keys():
    for key in settingsKeys:
        print(f"{key}")

@app.command()
def get(key: str):
    resp = getSetting(key)
    if resp is not None:
        print(f"{key}: {resp}")
    else:
        print(f"{key} not found")

@app.command()
def set(key: str, value: str):
    resp = setSetting(key, value)
    if resp:
        print(f"Set {key} to {value}")
    else:
        print(f"{key} not found")

@app.command()
def getSettings():
    with open(SETTINGSFILE, 'r') as f:
        settings = json.load(f)
    for k, v in settings.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    app()


