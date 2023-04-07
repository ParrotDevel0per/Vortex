import json
import time
import os
import shutil
from utils.paths import CACHE_FOLDER

cacheRegistry = os.path.join(CACHE_FOLDER, "registry.json")

def addToCacheRegistry(filename, folder, expiry):
    if not os.path.exists(cacheRegistry): open(cacheRegistry, 'w').write("{}")
    reg = json.load(open(cacheRegistry, 'r'))
    reg[f"{folder}-{filename}"] = {
        "filename": filename,
        "folder": folder,
        "expiry": time.time() + expiry
    }
    open(cacheRegistry, 'w').write(json.dumps(reg))

def removeFromCacheRegistry(filename, folder):
    if not os.path.exists(cacheRegistry): open(cacheRegistry, 'w').write("{}")
    reg = json.load(open(cacheRegistry, 'r'))
    if f"{folder}-{filename}" in reg:
        del reg[f"{folder}-{filename}"]
    open(cacheRegistry, 'w').write(json.dumps(reg))

def searchForExpiredItems():
    if not os.path.exists(cacheRegistry): open(cacheRegistry, 'w').write("{}")
    reg = json.load(open(cacheRegistry, 'r'))
    for key in reg:
        if reg[key]["expiry"] < time.time():
            removeFromCacheRegistry(reg[key]["filename"], reg[key]["folder"])
            file = os.path.join(CACHE_FOLDER, reg[key]['folder'], reg[key]['filename'])
            if os.path.exists(file):
                os.remove(file)
            #print(f"Removed {reg[key]['filename']} from {reg[key]['folder']}")

def cacheItem(filename, folder, data, expiry=(7 * 24 * 60 * 60)):
    if not data or data == "{}": return
    searchForExpiredItems()
    addToCacheRegistry(filename, folder, expiry)
    if not os.path.exists(os.path.join(CACHE_FOLDER, folder)): os.makedirs(os.path.join(CACHE_FOLDER, folder))
    with open(os.path.join(CACHE_FOLDER, folder, filename), 'w') as f:
        f.write(data)

def getCachedItem(filename, folder):
    searchForExpiredItems()
    if os.path.exists(os.path.join(CACHE_FOLDER, folder, filename)):
        with open(os.path.join(CACHE_FOLDER, folder, filename), 'r') as f:
            return f.read()
    return None

def getCacheSize():
    used = 0
    for folder, subfolders, filenames in os.walk(CACHE_FOLDER):
        for filename in filenames:
            used += os.path.getsize(os.path.join(folder, filename))
    return f"{round(used / (1024 * 1024), 2)}MB"

def clearCache():
    fileCount = len(os.listdir(CACHE_FOLDER))
    if fileCount == 0: return "0"
    shutil.rmtree(CACHE_FOLDER)
    os.makedirs(CACHE_FOLDER)
    return str(fileCount)