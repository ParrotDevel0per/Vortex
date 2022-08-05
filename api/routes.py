from flask import Blueprint, jsonify, Response, redirect, request, send_from_directory
from plugins.gomo import resolve as gomoResolve
import plugins.imdb as imdb
import requests
import shutil
import psutil
import json
import time
import os

api = Blueprint('api', __name__)
cachePosters = True
cacheFolder = ".cache"
DBFolder = "DB"
if not os.path.exists(cacheFolder): os.makedirs(cacheFolder)
if not os.path.exists(DBFolder): os.makedirs(DBFolder)

def chunkedDownload(url, filename, chunkSize=8192):
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunkSize):
            if chunk:
                f.write(chunk)
    return filename

def addToCacheRegistry(filename, folder):
    if not os.path.exists(f"{cacheFolder}/registry.json"): open(f"{cacheFolder}/registry.json", 'w').write("{}")
    reg = json.load(open(f"{cacheFolder}/registry.json", 'r'))
    reg[f"{folder}-{filename}"] = {
        "filename": filename,
        "folder": folder,
        "expiry": time.time() + (24 * 60 * 60)
    }
    open(f"{cacheFolder}/registry.json", 'w').write(json.dumps(reg))

def removeFromCacheRegistry(filename, folder):
    if not os.path.exists(f"{cacheFolder}/registry.json"): open(f"{cacheFolder}/registry.json", 'w').write("{}")
    reg = json.load(open(f"{cacheFolder}/registry.json", 'r'))
    if f"{folder}-{filename}" in reg:
        del reg[f"{folder}-{filename}"]
    open(f"{cacheFolder}/registry.json", 'w').write(json.dumps(reg))

def searchForExpiredItems():
    if not os.path.exists(f"{cacheFolder}/registry.json"): open(f"{cacheFolder}/registry.json", 'w').write("{}")
    reg = json.load(open(f"{cacheFolder}/registry.json", 'r'))
    for key in reg:
        if reg[key]["expiry"] < time.time():
            removeFromCacheRegistry(reg[key]["filename"], reg[key]["folder"])
            os.remove(f"{cacheFolder}/{reg[key]['folder']}/{reg[key]['filename']}")
            print(f"Removed {reg[key]['filename']} from {reg[key]['folder']}")

def cacheItem(filename, folder, data):
    searchForExpiredItems()
    addToCacheRegistry(filename, folder)
    if not os.path.exists(f"{cacheFolder}/{folder}"): os.makedirs(f"{cacheFolder}/{folder}")
    with open(f"{cacheFolder}/{folder}/{filename}", 'w') as f:
        f.write(data)

def getCachedItem(filename, folder):
    searchForExpiredItems()
    if os.path.exists(f"{cacheFolder}/{folder}/{filename}"):
        with open(f"{cacheFolder}/{folder}/{filename}", 'r') as f:
            return f.read()
    return None

def getRAMUsage(): return f"{psutil.virtual_memory().percent}%"

def getCPUUsage(): return f"{psutil.cpu_percent()}%"

def getCacheSize():
    used = 0
    for folder, subfolders, filenames in os.walk(cacheFolder):
        for filename in filenames:
            used += os.path.getsize(os.path.join(folder, filename))
    return f"{round(used / (1024 * 1024), 2)}MB"


@api.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'message': 'API Running'
    })

@api.route('/sysinfo')
def sysinfo():
    return jsonify({
        'status': 'ok',
        'systemRAMUsage': getRAMUsage(),
        'pythonCPUUsage': getCPUUsage(),
        'cache': getCacheSize(),
        'version': open('VERSION', 'r').read()
    })

@api.route('/resolve/<id>')
@api.route('/resolve/', defaults={'id': None})
def resolve(id):
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if not id.startswith("tt"): id = f"tt{id}"
    return jsonify({
        "id": id,
        "url": gomoResolve(f"https://gomo.to/movie/{id}")
    })

@api.route('/poster/<id>')
@api.route('/poster/', defaults={'id': None})
def poster(id):
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    do = request.args.get('do', None)
    posterURL = imdb.IMDBtoPoster(id)
    if not posterURL: posterURL = "/static/img/nopicture.jpg"
    if do == 'redirect': return redirect(posterURL)
    elif do == 'show':
        if not os.path.exists(f"{cacheFolder}/posters"): os.makedirs(f"{cacheFolder}/posters")
        if not cachePosters or "nopicture" in posterURL: return Response(requests.get(posterURL).content, mimetype="image/jpeg")
        if f"tt{id}.png" not in os.listdir(f"{cacheFolder}/posters"):
            chunkedDownload(posterURL, f"{cacheFolder}/posters/tt{id}.png")
        return send_from_directory(f"{cacheFolder}/posters", f"tt{id}.png")
    return jsonify({
        "id": id,
        "url": posterURL
    })

@api.route('/search/<query>')
@api.route('/search/', defaults={'query': None})
def search(query):
    if not query: return jsonify({
        'status': 'error',
        'message': 'No query provided'
    })
    cached = getCachedItem(f"search-query-{query.replace(' ', '---')}.json", "search")
    if cached == None:
        results = imdb.search(query)
        cacheItem(f"search-query-{query.replace(' ', '---')}.json", "search", json.dumps(results))
        return jsonify({
            "query": query,
            "results": results
        })
    print(f"Returning cached search results for \"{query}\"")
    return jsonify({
        "query": query,
        "results": json.loads(cached)
    })

@api.route('/top250movies/')
def top250movies():
    cached = getCachedItem("top250movies.json", "imdbCache")
    if cached == None:
        results = imdb.top250movies()
        cacheItem("top250movies.json", "imdbCache", json.dumps(results))
        return jsonify({
            "results": results
        })
    print("Returning cached top250movies.json")
    return jsonify({
        "results": json.loads(cached)
    })

@api.route('/bottom100movies/')
def bottom100movies():
    cached = getCachedItem("bottom100movies.json", "imdbCache")
    if cached == None:
        results = imdb.bottom100movies()
        cacheItem("bottom100movies.json", "imdbCache", json.dumps(results))
        return jsonify({
            "results": results
        })
    print("Returning cached bottom100movies.json")
    return jsonify({
        "results": json.loads(cached)
    })


@api.route('/favorites/')
def favorites():
    if not os.path.exists(f"{DBFolder}/favorites.json"): open(f"{DBFolder}/favorites.json", "w").write("{}")
    return json.loads(open(f"DB/favorites.json", "r").read())

@api.route('/addToFavorites/<id>')
@api.route('/addToFavorites/', defaults={'id': None})
def addToFavorites(id):
    if not os.path.exists(f"{DBFolder}/favorites.json"): open(f"{DBFolder}/favorites.json", "w").write("{}")
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    movie = imdb.getMovieInfo(id)
    favorites = json.loads(open(f"DB/favorites.json", "r").read())
    favorites[id] = {
        "title": movie["title"],
        "year": movie["year"],
        "poster": movie["full-size cover url"],
        "id": f"tt{id}"
    }
    open(f"DB/favorites.json", "w").write(json.dumps(favorites))
    return jsonify({
        "status": "ok",
        "message": "Movie added to favorites"
    })

@api.route('/removeFromFavorites/<id>')
@api.route('/removeFromFavorites/', defaults={'id': None})
def removeFromFavorites(id):
    if not os.path.exists(f"{DBFolder}/favorites.json"): open(f"{DBFolder}/favorites.json", "w").write("{}")
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    favorites = json.loads(open(f"DB/favorites.json", "r").read())
    if id in favorites:
        del favorites[id]
        open(f"DB/favorites.json", "w").write(json.dumps(favorites))
        return jsonify({
            "status": "ok",
            "message": "Movie removed from favorites"
        })
    return jsonify({
        "status": "error",
        "message": "Movie not found in favorites"
    })

@api.route('/isInFavorites/<id>')
@api.route('/isInFavorites/', defaults={'id': None})
def isInFavorites(id):
    if not os.path.exists(f"{DBFolder}/favorites.json"): open(f"{DBFolder}/favorites.json", "w").write("{}")
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    favorites = json.loads(open(f"DB/favorites.json", "r").read())
    if id in favorites:
        return jsonify({
            "status": "ok",
            "message": "Movie found in favorites"
        })
    return jsonify({
        "status": "error",
        "message": "Movie not found in favorites"
    })

@api.route('/clearPosterCache/')
def clearPosterCache():
    fileCount = len(os.listdir(f"{cacheFolder}/posters"))
    if fileCount == 0: return jsonify({
        'status': 'error',
        'message': 'No posters found'
    })
    shutil.rmtree(f"{cacheFolder}/posters")
    os.makedirs(f"{cacheFolder}/posters")
    return jsonify({
        "status": "ok",
        "message": "Poster cache cleared",
        "filesDeleted": fileCount
    })

@api.route('/clearCache/')
def clearCache():
    fileCount = len(os.listdir(f"{cacheFolder}"))
    if fileCount == 0: return jsonify({
        'status': 'error',
        'message': 'No files / folders found'
    })
    shutil.rmtree(f"{cacheFolder}")
    os.makedirs(f"{cacheFolder}")
    return jsonify({
        "status": "ok",
        "message": "Cache cleared",
        "filesDeleted": fileCount
    })

@api.route('/proxy/<path:url>')
def proxy(url):
    return requests.get(url).content