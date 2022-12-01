from flask import Blueprint, jsonify, request
from classes.imdb import IMDB
import threading
import json
from utils.cache import getCachedItem, cacheItem
from utils.users import userdata, changeValue, reqToUID

playlistRT = Blueprint('playlist', __name__)

@playlistRT.route('/playlist/')
def playlist():
    return jsonify({
        "results": userdata(reqToUID(request))["playlist"]
    })

def addToPlaylistThread(id, uid):
    movie = IMDB().getMovieInfo(id)
    playlist = userdata(uid)["playlist"]
    playlist[id] = {
        "title": movie['title'],
        "year": movie['year'],
        "poster": movie["full-size cover url"],
        "id": f"tt{id}"
    }
    changeValue(uid, "playlist", playlist)

@playlistRT.route('/addToPlaylist/<id>')
@playlistRT.route('/addToPlaylist/', defaults={'id': None})
def addToPlaylist(id):
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    threading.Thread(target=addToPlaylistThread, args=(id, reqToUID(request), )).start()
    return jsonify({
        "status": "ok",
        "message": "Movie added to playlist"
    })

@playlistRT.route('/removeFromPlaylist/<id>')
@playlistRT.route('/removeFromPlaylist/', defaults={'id': None})
def removeFromPlaylist(id):
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
    return jsonify({
        "status": "error",
        "message": "Movie not found in playlist"
    })

@playlistRT.route('/isInPlaylist/<id>')
@playlistRT.route('/isInPlaylist/', defaults={'id': None})
def isInPlaylist(id):
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
    return jsonify({
        "status": "error",
        "message": "Movie not found in playlist"
    })

@playlistRT.route('/seriesToPlaylist/<id>')
@playlistRT.route('/seriesToPlaylist/', defaults={'id': None})
def serieasToPlaylist(id):
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