from flask import Blueprint, request, render_template, send_from_directory, redirect
from utils.paths import DB_FOLDER
from utils.settings import getSetting
import requests
import json
import os

www = Blueprint('www', __name__)
playlistFile = os.path.join(DB_FOLDER, "playlist.json")


def getPreloader():
    return f"/static/img/preloader/{getSetting('preloader')}"

@www.route('/')
def index():
    return render_template('index.html')

@www.route('/play/<id>/<episode>')
@www.route('/play/<id>', defaults={'episode': None})
def play(id, episode):
    source = getSetting('source')
    if request.args.get('source'): source = request.args.get('source')
    baseURL = request.base_url.split('/play')[0]
    url = f"{baseURL}/api/resolve/{id}?source={source}"
    if episode: url += f"?episode={episode}"
    #try: resolved = requests.get(url).json()["url"]
    #except: resolved = ""
    movieInfoURL = f""
    if episode: movieInfoURL += f"{baseURL}/api/getEpisodeInfo/{id}/{episode}"
    else: movieInfoURL += f"{baseURL}/api/getMovieInfo/{id}"
    metadata = requests.get(movieInfoURL).json()
    resolved = requests.get(url).json()["url"]
    return render_template('play.html', url=url, id=id, preloader=getPreloader(), metadata=metadata, resolved=resolved)

@www.route('/play/<id>.m3u8')
def play_m3u8(id):
    source = getSetting('source')
    if request.args.get('source'): source = request.args.get('source')
    try: resolved = requests.get(f"{request.base_url.split('/play')[0]}/api/resolve/{id}?source={source}").json()["url"]
    except: resolved = ""
    return redirect(resolved, code=302)

@www.route('/play/<id>/<episode>.m3u8')
def play_m3u8_episode(id, episode):
    source = getSetting('source')
    if request.args.get('source'): source = request.args.get('source')
    try: resolved = requests.get(f"{request.base_url.split('/play')[0]}/api/resolve/{id}?episode={episode}&source={source}").json()["url"]
    except: resolved = ""
    return redirect(resolved, code=302)

@www.route('/search')
def search():
    return render_template('search.html')

@www.route('/seasons/<id>')
def seasons(id):
    try: results = requests.get(f"{request.base_url.split('/seasons')[0]}/api/seasons/{id}").json()
    except: results = []
    title = results["results"]["title"]
    seasons = results["results"]["seasons"]
    return render_template('seasons.html', id=id, iterator=range(seasons), seasons=seasons, title=title)

@www.route('/episodes/<id>/<season>')
def episodes(id, season):
    try: results = requests.get(f"{request.base_url.split('/episodes')[0]}/api/episodes/{id}/{season}").json()
    except: results = []
    title = results["results"]["title"]
    del results["results"]["title"]
    del results["results"]["poster"]
    episodes = results["results"]
    return render_template('episodes.html', id=id, title=title, episodes=episodes, count=len(episodes), season=season)

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
    source = getSetting('source')
    if request.args.get('source'): source = request.args.get('source')
    j = json.load(open(playlistFile))
    baseURL = request.base_url.split('/playlist')[0]
    proxifyPoster = getSetting("proxifyM3UPosters")
    m3u = "#EXTM3U\n"
    for i in j:
        title = f'[{j[i]["year"]}] {j[i]["title"]}'
        id = j[i]["id"]
        poster = j[i]["poster"]
        if proxifyPoster: poster = f"{baseURL}/api/poster/{id}?do=show"
        m3u += f'#EXTINF:-1 tvg-logo="{poster}" tvg-id="{id}" tvg-name="{title}", {title}\n{baseURL}/play/{id}.m3u8?source={source}\n'
    return m3u

@www.route('/show/<id>.m3u')
def showm3u(id):
    if not os.path.exists(playlistFile):
        return "Playlist file not found"
    source = getSetting('source')
    if request.args.get('source'): source = request.args.get('source')
    baseURL = request.base_url.split('/show')[0]
    resp = requests.get(f"{baseURL}/api/seriesToPlaylist/{id}").json()
    poster = resp["poster"]
    if getSetting("proxifyM3UPosters"):
        poster = f"{baseURL}/api/poster/{id}?do=show"
    m3u = "#EXTM3U\n"
    for season in resp["seasons"]:
        for episode in resp["seasons"][season]:
            title = resp["seasons"][season][episode]["title"]
            group = resp["seasons"][season][episode]["group"]
            m3u += f'#EXTINF:-1 tvg-logo="{poster}" tvg-id="{id}" tvg-name="{title}" group-title="{group}", {title}\n{baseURL}/play/{id}/{season}-{episode}.m3u8?source={source}\n'
    return m3u

@www.route('/mergeShowM3Us')
def mergeShowM3Us():
    return render_template('mergeShowPlaylists.html')