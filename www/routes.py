from flask import Blueprint, request, render_template, send_from_directory
import requests

www = Blueprint('www', __name__)

@www.route('/')
def index():
    return render_template('index.html')

@www.route('/play/<id>')
def play(id):
    try: resolved = requests.get(f"{request.base_url.split('/play')[0]}/api/resolve/{id}").json()["url"]
    except: resolved = ""
    return render_template('play.html', url=resolved, id=id)

@www.route('/search')
def search():
    return render_template('search.html')

@www.route('/top250movies')
def top250movies():
    results = requests.get(f"{request.base_url.split('/top250movies')[0]}/api/top250movies/").json()["results"]
    return render_template('movieList.html', results=results, title="Top 250 IMDB Movies", count=len(results))

@www.route('/bottom100movies')
def bottom100movies():
    results = requests.get(f"{request.base_url.split('/bottom100movies')[0]}/api/bottom100movies/").json()["results"]
    return render_template('movieList.html', results=results, title="Bottom 100 IMDB Movies", count=len(results))

@www.route('/favorites')
def favorites():
    results = requests.get(f"{request.base_url.split('/favorites')[0]}/api/favorites/").json()
    return render_template('movieList.html', results=results, title="Favorites", count=len(results))

@www.route('/playWithIMDBID')
def playWithIMDBID():
    return render_template('playWithIMDBId.html')

@www.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)