from flask import Blueprint, jsonify, request
import plugins.imdb as imdb
import threading
import json
from utils.users import verify, userdata, changeValue, reqToUID

favoritesRT = Blueprint('favorites', __name__)

@favoritesRT.route('/favorites/')
def favorites():
    if verify(request) == False: return "Forbidden", 403

    return jsonify({
        "results": userdata(reqToUID(request))["favorites"]
    })

def addToFavsThread(id, uid):
    movie = imdb.getMovieInfo(id)
    favorites = userdata(uid)["favorites"]
    favorites[id] = {
        "title": movie["title"],
        "year": movie["year"],
        "poster": movie["full-size cover url"],
        "id": f"tt{id}",
        "kind": movie["kind"]
    }
    changeValue(uid, "favorites", favorites)

@favoritesRT.route('/addToFavorites/<id>')
@favoritesRT.route('/addToFavorites/', defaults={'id': None})
def addToFavorites(id):
    if verify(request) == False: return "Forbidden", 403

    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    threading.Thread(target=addToFavsThread, args=(id, reqToUID(request), )).start()
    return jsonify({
        "status": "ok",
        "message": "Movie added to favorites"
    })

@favoritesRT.route('/removeFromFavorites/<id>')
@favoritesRT.route('/removeFromFavorites/', defaults={'id': None})
def removeFromFavorites(id):
    if verify(request) == False: return "Forbidden", 403

    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    favorites = userdata(reqToUID(request))["favorites"]
    if id in favorites:
        del favorites[id]
        changeValue(reqToUID(request), "favorites", favorites)
        return jsonify({
            "status": "ok",
            "message": "Movie removed from favorites"
        })
    return jsonify({
        "status": "error",
        "message": "Movie not found in favorites"
    })

@favoritesRT.route('/isInFavorites/<id>')
@favoritesRT.route('/isInFavorites/', defaults={'id': None})
def isInFavorites(id):
    if verify(request) == False: return "Forbidden", 403
    

    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    favorites = userdata(reqToUID(request))["favorites"]
    if id in favorites:
        return jsonify({
            "status": "ok",
            "message": "Movie found in favorites"
        })
    return jsonify({
        "status": "error",
        "message": "Movie not found in favorites"
    })