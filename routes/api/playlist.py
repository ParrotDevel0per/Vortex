from flask import Blueprint, jsonify, request
from classes.imdb import IMDB
import threading
import json
from utils.cache import getCachedItem, cacheItem
from utils.users import userdata, changeValue, reqToUID

playlistRT = Blueprint('playlist', __name__)

def createPlaylistDict(uid):
    data = userdata(uid)
    if "playlist" not in data:
        changeValue(uid, "playlist", {})

    if "playlisttv" not in data:
        changeValue(uid, "playlisttv", {})

@playlistRT.route('/playlist/')
def playlisttv():
    createPlaylistDict(reqToUID(request))
    return jsonify({
        "results": userdata(reqToUID(request))["playlist"]
    })

@playlistRT.route('/playlisttv/')
def playlist():
    createPlaylistDict(reqToUID(request))
    return jsonify({
        "results": userdata(reqToUID(request))["playlisttv"]
    })

def addToPlaylistThread(id, uid):
    movie = IMDB().getMovieInfo(id)
    show = "number of seasons" in movie

    playlist = userdata(uid)["playlisttv" if show else "playlist"]
    playlist[id] = {
        "title": movie['title'],
        "year": movie['year'] if 'year' in movie else '0',
        "poster": movie["full-size cover url"],
        "id": f"tt{id}"
    }
    changeValue(uid, "playlisttv" if show else "playlist", playlist)

@playlistRT.route('/addToPlaylist/<id>')
@playlistRT.route('/addToPlaylist/', defaults={'id': None})
def addToPlaylist(id):
    createPlaylistDict(reqToUID(request))
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    threading.Thread(target=addToPlaylistThread, args=(id, reqToUID(request), )).start()
    return jsonify({
        "status": "ok",
        "message": "Item added to playlist"
    })

@playlistRT.route('/removeFromPlaylist/<id>')
@playlistRT.route('/removeFromPlaylist/', defaults={'id': None})
def removeFromPlaylist(id):
    createPlaylistDict(reqToUID(request))
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    playlist = userdata(reqToUID(request))["playlist"]
    if id.startswith("tt"): id = id[2:]
    if id in playlist:
        del playlist[id]
        changeValue(reqToUID(request), "playlist", playlist)
        return jsonify({
            "status": "ok",
            "message": "Movie removed from playlist"
        })

    playlisttv = userdata(reqToUID(request))["playlisttv"]
    if id in playlisttv:
        del playlisttv[id]
        changeValue(reqToUID(request), "playlisttv", playlisttv)
        return jsonify({
            "status": "ok",
            "message": "Show removed from playlist"
        })

    return jsonify({
        "status": "error",
        "message": "Movie not found in playlist"
    })

@playlistRT.route('/isInPlaylist/<id>')
@playlistRT.route('/isInPlaylist/', defaults={'id': None})
def isInPlaylist(id):
    createPlaylistDict(reqToUID(request))
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    playlist = userdata(reqToUID(request))["playlist"]
    if id in playlist:
        return jsonify({
            "status": "ok",
            "message": "Movie found in playlist"
        })

    playlisttv = userdata(reqToUID(request))["playlisttv"]
    if id in playlisttv:
        return jsonify({
            "status": "ok",
            "message": "Movie found in playlist"
        })
    return jsonify({
        "status": "error",
        "message": "Movie not found in playlist"
    })

@playlistRT.route('/seriesToPlaylist/<id>')
@playlistRT.route('/seriesToPlaylist/', defaults={'id': None})
def seriesToPlaylist(id):
    createPlaylistDict(reqToUID(request))
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    #pl = imdb.createPlaylistFromSeries(id)
    cache = getCachedItem(f"playlist-{id}.json", "playlists")
    if cache == None:
        pl = IMDB().createPlaylistFromSeries(id)
        cacheItem(f"playlist-{id}.json", "playlists", json.dumps(pl), expiry=(24 * 60 * 60 * 7))
        return pl
    #print(f"Returning cached playlist for \"{id}\"")
    return json.loads(cache)