from flask import Blueprint, jsonify
import plugins.imdb as imdb
import threading
import json
from utils.paths import DB_FOLDER
from utils.cache import getCachedItem, cacheItem
import os

playlistRT = Blueprint('playlist', __name__)
playlistFile = os.path.join(DB_FOLDER, "playlist.json")

@playlistRT.route('/playlist/')
def playlist():
    if not os.path.exists(playlistFile): open(playlistFile, "w").write("{}")
    return jsonify({
        "results": json.loads(open(playlistFile, "r").read())
    })

def addToPlaylistThread(id):
    movie = imdb.getMovieInfo(id)
    playlist = json.loads(open(playlistFile, "r").read())
    playlist[id] = {
        "title": movie['title'],
        "year": movie['year'],
        "poster": movie["full-size cover url"],
        "id": f"tt{id}"
    }
    open(playlistFile, "w").write(json.dumps(playlist))

@playlistRT.route('/addToPlaylist/<id>')
@playlistRT.route('/addToPlaylist/', defaults={'id': None})
def addToPlaylist(id):
    if not os.path.exists(playlistFile): open(playlistFile, "w").write("{}")
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    threading.Thread(target=addToPlaylistThread, args=(id,)).start()
    return jsonify({
        "status": "ok",
        "message": "Movie added to playlist"
    })

@playlistRT.route('/removeFromPlaylist/<id>')
@playlistRT.route('/removeFromPlaylist/', defaults={'id': None})
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

@playlistRT.route('/isInPlaylist/<id>')
@playlistRT.route('/isInPlaylist/', defaults={'id': None})
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

@playlistRT.route('/seriesToPlaylist/<id>')
@playlistRT.route('/seriesToPlaylist/', defaults={'id': None})
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
        cacheItem(f"playlist-{id}.json", "playlists", json.dumps(pl), expiry=(24 * 60 * 60 * 7))
        return pl
    #print(f"Returning cached playlist for \"{id}\"")
    return json.loads(cache)