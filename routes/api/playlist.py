from flask import Blueprint, jsonify, request
from classes.imdb import IMDB
import threading
import json
from utils.cache import getCachedItem, cacheItem
from utils.users import reqToUID
from utils.common import randStr
import os
from utils.paths import DB_FOLDER
from urllib.parse import unquote

playlistRT = Blueprint('playlist', __name__)
playlistsFile = os.path.join(DB_FOLDER, "playlists.json")
if not os.path.exists(playlistsFile):
    open(playlistsFile, "w", encoding="utf-8").write("{}")


"""
# Playlists file structure
{
    "playlistID": {
        "title": "Movies",
        "owners": [],
        "playlistID": "",
        "public": True,
        "count": 0,
        "items": {
            "movieID": {
                "title": "",
                "year": "",
                "poster": "",
                "id": "",
                "kind": ""
            }
        }
    }

}

"""

def ok(msg):
    return jsonify({
        'status': 'ok',
        'message': msg
    })

def error(msg):
    return jsonify({
        'status': 'error',
        'message': msg
    })


@playlistRT.route('/createPlaylist')
def createPlaylist():
    uid = reqToUID(request)
    loaded = json.load(open(playlistsFile))

    playlistID = randStr(length=32, incUpper=True)
    loaded[playlistID] = {
        "title": request.args.get("title", "Playlist"),
        "owners": [uid],
        "playlistID": playlistID,
        "public": True,
        "count": 0,
        "logo": "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse3.mm.bing.net%2Fth%3Fid%3DOIP.KDhva9uM2b3jvBQSLw-3hwHaGB%26pid%3DApi&f=1&ipt=4fd55b6b6f2a5ad2da5fd2c02809925578cd105cf30a6374222800227c8463ed&ipo=images",
        "items": {}
    }
    open(playlistsFile, "w", encoding="utf-8").write(json.dumps(loaded))
    return ok("Created playlist")


@playlistRT.route('/renamePlaylist')
def renamePlaylist():
    playlistID = request.args.get("playlistID")
    title = request.args.get("title")

    if not playlistID or not title:
        return error("Invalid request")

    loaded = json.load(open(playlistsFile))
    uid = reqToUID(request)

    if playlistID not in loaded:
        return error("Playlist does not exist")

    if uid not in loaded[playlistID]["owners"]:
        return error("You are not authenticated to do that")

    loaded[playlistID]["title"] = title
    open(playlistsFile, "w", encoding="utf-8").write(json.dumps(loaded))

    return ok("Successfully renamed playlist")

@playlistRT.route('/changeIcon')
def changeIcon():
    playlistID = request.args.get("playlistID")
    image = request.args.get("image")

    if not playlistID or not image:
        return error("Invalid request")

    loaded = json.load(open(playlistsFile))
    uid = reqToUID(request)

    if playlistID not in loaded:
        return error("Playlist does not exist")

    if uid not in loaded[playlistID]["owners"]:
        return error("You are not authenticated to do that")

    loaded[playlistID]["logo"] = unquote(image)
    open(playlistsFile, "w", encoding="utf-8").write(json.dumps(loaded))

    return ok("Successfully renamed playlist")


@playlistRT.route('/deletePlaylist/<playlistID>')
@playlistRT.route('/deletePlaylist', defaults={"playlistID": None})
def deletePlaylist(playlistID):
    if not playlistID:
        return error("No ID provided")

    loaded = json.load(open(playlistsFile))
    uid = reqToUID(request)

    if playlistID not in loaded:
        return error("Playlist does not exist")

    if uid not in loaded[playlistID]["owners"]:
        return error("You are not authenticated to do that")

    del loaded[playlistID]
    open(playlistsFile, "w", encoding="utf-8").write(json.dumps(loaded))

    return ok("Successfully deleted playlist")


@playlistRT.route('/playlist/<playlistID>')
@playlistRT.route('/playlist', defaults={"playlistID": None})
def playlist(playlistID):
    if not playlistID:
        return error("No ID provided")

    loaded = json.load(open(playlistsFile))

    if playlistID not in loaded:
        return error("Playlist does not exist")

    return jsonify({
        "results": loaded[playlistID]
    })

@playlistRT.route('/playlists')
def playlists():
    uid = reqToUID(request)
    loaded = json.load(open(playlistsFile))
    response = {}

    for playlistID, playlistData in loaded.items():
        if uid in playlistData["owners"]:
            response[playlistID] = playlistData


    return jsonify({
        "results": response
    })


def addToPlaylistThread(playlistID, imdbID):
    movie = IMDB().getMovieInfo(imdbID)

    loaded = json.load(open(playlistsFile))
    loaded[playlistID]["items"][imdbID] = {
        "title": movie['title'],
        "year": movie['year'] if 'year' in movie else '0',
        "poster": movie["full-size cover url"],
        "id": f"tt{imdbID}",
        "kind": "show" if "number of seasons" in movie else "movie"
    }

    loaded[playlistID]["count"] += 1
    open(playlistsFile, "w", encoding="utf-8").write(json.dumps(loaded))



@playlistRT.route('/addToPlaylist/<playlistID>/<imdbID>')
@playlistRT.route('/addToPlaylist/', defaults={'playlistID': None, 'imdbID': None})
def addToPlaylist(playlistID, imdbID):
    if not playlistID or not imdbID:
        return error("No ID provided")

    if imdbID.startswith("tt"):
        imdbID = imdbID[2:]

    loaded = json.load(open(playlistsFile))
    uid = reqToUID(request)

    if playlistID not in loaded:
        return error("Playlist does not exist")

    if uid not in loaded[playlistID]["owners"]:
        return error("You are not authenticated to do that")

    threading.Thread(target=addToPlaylistThread, args=(playlistID, imdbID, )).start()
    return ok("Item added to playlist")

@playlistRT.route('/removeFromPlaylist/<playlistID>/<imdbID>')
@playlistRT.route('/removeFromPlaylist/', defaults={'playlistID': None, 'imdbID': None})
def removeFromPlaylist(playlistID, imdbID):
    if not playlistID or not imdbID:
        return error("No ID provided")

    if imdbID.startswith("tt"):
        imdbID = imdbID[2:]

    loaded = json.load(open(playlistsFile))
    uid = reqToUID(request)

    if playlistID not in loaded:
        return error("Playlist does not exist")

    if uid not in loaded[playlistID]["owners"]:
        return error("You are not authenticated to do t")

    if imdbID not in loaded[playlistID]["items"]:
        return error("Item is not in playlist")
    
    del loaded[playlistID]["items"][imdbID]
    loaded[playlistID]["count"] -= 1
    open(playlistsFile, "w", encoding="utf-8").write(json.dumps(loaded))
    return ok("Successfully removed item from playlist")



@playlistRT.route('/seriesToPlaylist/<id>')
@playlistRT.route('/seriesToPlaylist/', defaults={'id': None})
def seriesToPlaylist(id):
    if not id: 
        return error("No ID provided")
    if id.startswith("tt"): id = id[2:]
    #pl = imdb.createPlaylistFromSeries(id)
    cache = getCachedItem(f"playlist-{id}.json", "playlists")
    if cache == None:
        pl = IMDB().createPlaylistFromSeries(id)
        cacheItem(f"playlist-{id}.json", "playlists", json.dumps(pl), expiry=(24 * 60 * 60 * 7))
        return pl
    #print(f"Returning cached playlist for \"{id}\"")
    return json.loads(cache)