from flask import Blueprint, jsonify, Response, redirect, request, send_from_directory
from plugins.gomo import resolve as gomoResolve
from plugins.vidsrc import resolve as vidsrcResolve
from settings import getSetting
import plugins.imdb as imdb
import requests
import shutil
import psutil
import json
import time
from utils.paths import CACHE_FOLDER, DB_FOLDER
import os

api = Blueprint('api', __name__)
cachePosters = bool(getSetting("cachePosters"))
cacheRegistry = os.path.join(CACHE_FOLDER, "registry.json")
postersFolder = os.path.join(CACHE_FOLDER, "posters")
favoritesFile = os.path.join(DB_FOLDER, "favorites.json")
playlistFile = os.path.join(DB_FOLDER, "playlist.json")

def chunkedDownload(url, filename, chunkSize=8192):
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunkSize):
            if chunk:
                f.write(chunk)
    return filename

def addToCacheRegistry(filename, folder):
    if not os.path.exists(cacheRegistry): open(cacheRegistry, 'w').write("{}")
    reg = json.load(open(cacheRegistry, 'r'))
    reg[f"{folder}-{filename}"] = {
        "filename": filename,
        "folder": folder,
        "expiry": time.time() + (24 * 60 * 60)
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
            os.remove(os.path.join(CACHE_FOLDER, reg[key]['folder'], reg[key]['filename']))
            print(f"Removed {reg[key]['filename']} from {reg[key]['folder']}")

def cacheItem(filename, folder, data):
    searchForExpiredItems()
    addToCacheRegistry(filename, folder)
    if not os.path.exists(os.path.join(CACHE_FOLDER, folder)): os.makedirs(os.path.join(CACHE_FOLDER, folder))
    with open(os.path.join(CACHE_FOLDER, folder, filename), 'w') as f:
        f.write(data)

def getCachedItem(filename, folder):
    searchForExpiredItems()
    if os.path.exists(os.path.join(CACHE_FOLDER, folder, filename)):
        with open(os.path.join(CACHE_FOLDER, folder, filename), 'r') as f:
            return f.read()
    return None

def getRAMUsage(): return f"{psutil.virtual_memory().percent}%"

def getCPUUsage(): return f"{psutil.cpu_percent()}%"

def getCacheSize():
    used = 0
    for folder, subfolders, filenames in os.walk(CACHE_FOLDER):
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
    use = getSetting("source")
    if request.args.get("source"): use = request.args.get("source")
    episode = str(request.args.get("episode") or "")
    baseURL = request.base_url.split("/api")[0]
    sources = {
        "gomo": "gomoResolve(baseURL, id, episode)",
        "vidsrc": "vidsrcResolve(baseURL, id, episode)"
    }
    source = eval(sources[use])
    return jsonify({
        "id": id,
        "url": source
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
    baseURL = request.base_url.split('/api')[0]
    posterURL = imdb.IMDBtoPoster(id)
    if not posterURL: posterURL = f"{baseURL}/static/img/nopicture.jpg"
    if do == 'redirect': return redirect(posterURL)
    elif do == 'show':
        if not os.path.exists(postersFolder): os.makedirs(postersFolder)
        if not cachePosters or "nopicture" in posterURL: return Response(requests.get(posterURL).content, mimetype="image/jpeg")
        if f"tt{id}.png" not in os.listdir(postersFolder):
            chunkedDownload(posterURL, os.path.join(postersFolder, f"tt{id}.png"))
        return send_from_directory(postersFolder, f"tt{id}.png")
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

@api.route('/seasons/<id>')
@api.route('/seasons/', defaults={'id': None})
def seasons(id):
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    cached = getCachedItem(f"seasons-{id}.json", "seasons")
    if cached == None:
        results = imdb.seasons(id)
        cacheItem(f"seasons-{id}.json", "seasons", json.dumps(results))
        return jsonify({
            "id": id,
            "results": results
        })
    print(f"Returning cached seasons for \"{id}\"")
    return jsonify({
        "id": id,
        "results": json.loads(cached)
    })

@api.route('/episodes/<id>/<season>')
@api.route('/episodes/', defaults={'id': None, 'season': None})
def episodes(id, season):
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if season == None: return jsonify({
        'status': 'error',
        'message': 'No season provided'
    })
    if id.startswith("tt"): id = id[2:]
    if not season: return jsonify({
        'status': 'error',
        'message': 'No season provided'
    })
    cached = getCachedItem(f"episodes-{id}-{season}.json", "episodes")
    if cached == None:
        results = imdb.episodes(id, season)
        cacheItem(f"episodes-{id}-{season}.json", "episodes", json.dumps(results))
        return jsonify({
            "id": id,
            "season": season,
            "results": results
        })
    print(f"Returning cached episodes for \"{id}\"")
    return jsonify({
        "id": id,
        "season": season,
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

@api.route('/seriesToPlaylist/<id>')
@api.route('/seriesToPlaylist/', defaults={'id': None})
def serieasToPlaylist(id):
    if not os.path.exists(playlistFile): open(playlistFile, "w").write("{}")
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    #pl = imdb.createPlaylistFromSeries(id)
    cache = getCachedItem(f"playlist-{id}.json", "playlists")
    if cache == None:
        pl = imdb.createPlaylistFromSeries(id)
        cacheItem(f"playlist-{id}.json", "playlists", json.dumps(pl))
        return pl
    print(f"Returning cached playlist for \"{id}\"")
    return json.loads(cache)

@api.route('/favorites/')
def favorites():
    if not os.path.exists(favoritesFile): open(favoritesFile, "w").write("{}")
    return json.loads(open(favoritesFile, "r").read())

@api.route('/addToFavorites/<id>')
@api.route('/addToFavorites/', defaults={'id': None})
def addToFavorites(id):
    if not os.path.exists(favoritesFile): open(favoritesFile, "w").write("{}")
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    movie = imdb.getMovieInfo(id)
    favorites = json.loads(open(favoritesFile, "r").read())
    favorites[id] = {
        "title": movie["title"],
        "year": movie["year"],
        "poster": movie["full-size cover url"],
        "id": f"tt{id}",
        "kind": movie["kind"]
    }
    open(favoritesFile, "w").write(json.dumps(favorites))
    return jsonify({
        "status": "ok",
        "message": "Movie added to favorites"
    })

@api.route('/removeFromFavorites/<id>')
@api.route('/removeFromFavorites/', defaults={'id': None})
def removeFromFavorites(id):
    if not os.path.exists(favoritesFile): open(favoritesFile, "w").write("{}")
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    favorites = json.loads(open(favoritesFile, "r").read())
    if id in favorites:
        del favorites[id]
        open(favoritesFile, "w").write(json.dumps(favorites))
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
    if not os.path.exists(favoritesFile): open(favoritesFile, "w").write("{}")
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    favorites = json.loads(open(favoritesFile, "r").read())
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
    fileCount = len(os.listdir(postersFolder))
    if fileCount == 0: return jsonify({
        'status': 'error',
        'message': 'No posters found'
    })
    shutil.rmtree(postersFolder)
    os.makedirs(postersFolder)
    return jsonify({
        "status": "ok",
        "message": "Poster cache cleared",
        "filesDeleted": fileCount
    })

@api.route('/clearCache/')
def clearCache():
    fileCount = len(os.listdir(CACHE_FOLDER))
    if fileCount == 0: return jsonify({
        'status': 'error',
        'message': 'No files / folders found'
    })
    shutil.rmtree(CACHE_FOLDER)
    os.makedirs(CACHE_FOLDER)
    return jsonify({
        "status": "ok",
        "message": "Cache cleared",
        "filesDeleted": fileCount
    })

@api.route('/proxy/<path:url>')
def proxy(url):
    #return requests.get(url).content
    r = requests.get(url, stream=True)
    return Response(r.iter_content(chunk_size=10*1024),
                    content_type=r.headers['Content-Type'])

@api.route('/playlist/')
def playlist():
    if not os.path.exists(playlistFile): open(playlistFile, "w").write("{}")
    return json.loads(open(playlistFile, "r").read())

@api.route('/addToPlaylist/<id>')
@api.route('/addToPlaylist/', defaults={'id': None})
def addToPlaylist(id):
    if not os.path.exists(playlistFile): open(playlistFile, "w").write("{}")
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    movie = imdb.getMovieInfo(id)
    playlist = json.loads(open(playlistFile, "r").read())
    playlist[id] = {
        "title": movie['title'],
        "year": movie['year'],
        "poster": movie["full-size cover url"],
        "id": f"tt{id}"
    }
    open(playlistFile, "w").write(json.dumps(playlist))
    return jsonify({
        "status": "ok",
        "message": "Movie added to playlist"
    })

@api.route('/removeFromPlaylist/<id>')
@api.route('/removeFromPlaylist/', defaults={'id': None})
def removeFromPlaylist(id):
    if not os.path.exists(playlistFile): open(playlistFile, "w").write("{}")
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    playlist = json.loads(open(playlistFile, "r").read())
    if id in playlist:
        del playlist[id]
        open(playlistFile, "w").write(json.dumps(playlist))
        return jsonify({
            "status": "ok",
            "message": "Movie removed from playlist"
        })
    return jsonify({
        "status": "error",
        "message": "Movie not found in playlist"
    })

@api.route('/isInPlaylist/<id>')
@api.route('/isInPlaylist/', defaults={'id': None})
def isInPlaylist(id):
    if not os.path.exists(playlistFile): open(playlistFile, "w").write("{}")
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    playlist = json.loads(open(playlistFile, "r").read())
    if id in playlist:
        return jsonify({
            "status": "ok",
            "message": "Movie found in playlist"
        })
    return jsonify({
        "status": "error",
        "message": "Movie not found in playlist"
    })

@api.route('/mergeShows.m3u')
def mergeShowM3Us():
    baseURL = request.base_url.split("/api")[0]
    items = request.args.get("ids")
    if "|" in items: items = items.split("|")
    else: items = [items]
    m3u = "#EXTM3U\n"
    for id in items: m3u += requests.get(f"{baseURL}/show/{id}.m3u").text.replace("#EXTM3U\n", "")
    return Response(m3u, mimetype="audio/x-mpegurl")