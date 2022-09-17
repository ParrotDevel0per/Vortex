from flask import Blueprint, jsonify
import plugins.imdb as imdb
import threading
import json
from utils.paths import DB_FOLDER
import os

favoritesRT = Blueprint('favorites', __name__)
favoritesFile = os.path.join(DB_FOLDER, "favorites.json")

@favoritesRT.route('/favorites/')
def favorites():
    if not os.path.exists(favoritesFile): open(favoritesFile, "w").write("{}")
    return jsonify({
        "results": json.loads(open(favoritesFile, "r").read())
    })

def addToFavsThread(id):
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

@favoritesRT.route('/addToFavorites/<id>')
@favoritesRT.route('/addToFavorites/', defaults={'id': None})
def addToFavorites(id):
    if not os.path.exists(favoritesFile): open(favoritesFile, "w").write("{}")
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    threading.Thread(target=addToFavsThread, args=(id,)).start()
    return jsonify({
        "status": "ok",
        "message": "Movie added to favorites"
    })

@favoritesRT.route('/removeFromFavorites/<id>')
@favoritesRT.route('/removeFromFavorites/', defaults={'id': None})
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

@favoritesRT.route('/isInFavorites/<id>')
@favoritesRT.route('/isInFavorites/', defaults={'id': None})
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