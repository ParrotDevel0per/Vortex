from flask import Blueprint, request, render_template, send_from_directory, redirect
from utils.paths import DB_FOLDER
import requests
import json
import os

www = Blueprint('www', __name__)
playlistFile = os.path.join(DB_FOLDER, "playlist.json")

@www.route('/')
def index():
    return render_template('index.html')

@www.route('/play/<id>')
def play(id):
    try: resolved = requests.get(f"{request.base_url.split('/play')[0]}/api/resolve/{id}").json()["url"]
    except: resolved = ""
    return render_template('play.html', url=resolved, id=id)

@www.route('/play/<id>.m3u8')
def play_m3u8(id):
    try: resolved = requests.get(f"{request.base_url.split('/play')[0]}/api/resolve/{id}").json()["url"]
    except: resolved = ""
    return redirect(resolved, code=302)

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

@www.route('/playlist')
def playlist():
    results = requests.get(f"{request.base_url.split('/playlist')[0]}/api/playlist/").json()
    return render_template('movieList.html', results=results, title="Playlist", count=len(results))

@www.route('/playlist.m3u')
def playlistm3u8():
    if not os.path.exists(playlistFile):
        return "Playlist file not found"
    j = json.load(open(playlistFile))
    baseURL = request.base_url.split('/playlist')[0]
    proxifyPoster = True
    m3u = "#EXTM3U\n"
    for i in j:
        title = f'[{j[i]["year"]}] {j[i]["title"]}'
        id = j[i]["id"]
        poster = j[i]["poster"]
        if proxifyPoster: poster = f"{baseURL}/api/poster/{id}?do=show"
        m3u += f'#EXTINF:-1 tvg-logo="{poster}" tvg-id="{id}" tvg-name="{title}", {title}\n{baseURL}/play/{id}.m3u8\n'
    return m3u
