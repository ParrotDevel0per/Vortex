from utils.paths import DB_FOLDER
import os
import json

# https://stackoverflow.com/questions/34327719/get-keys-from-json-in-python
def get_simple_keys(data):
    result = []
    for key in data.keys():
        if type(data[key]) != dict:
            result.append(key)
        else:
            result += get_simple_keys(data[key])
    return result


ADDONSETTINGSFILE = os.path.join(DB_FOLDER, "addonsettings.json")
if not os.path.exists(ADDONSETTINGSFILE):
    open(ADDONSETTINGSFILE, "w").write("{}")


def getAddonSetting(addonid, key):
    with open(ADDONSETTINGSFILE, 'r') as f:
        settings = json.load(f)
        if addonid not in settings:
            return ""
        if key not in settings[addonid]:
            return ""
        return settings[addonid][key]


def setAddonSetting(addonid, key, value):
    with open(ADDONSETTINGSFILE, 'r') as f:
        settings = json.load(f)
        if addonid not in settings:
            settings[addonid] = {}
        settings[addonid][key] = value
        open(ADDONSETTINGSFILE, 'w').write(json.dumps(settings))
        return f"{key} is now {value}"




