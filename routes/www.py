from flask import Blueprint, request, render_template, send_from_directory, redirect
from utils.paths import DB_FOLDER
from utils.settings import getSetting
import requests
import json
import os

www = Blueprint('www', __name__)
playlistFile = os.path.join(DB_FOLDER, "playlist.json")

@www.route('/')
def index():
    return render_template(
        'index.html',
        tab=request.args.get("tab") or "",
        id=request.args.get("id") or "",
        showG=request.args.get("showG") or "true",
        kind = request.args.get("kind") or "",
        showFt = request.args.get("showFt") or "true",
    )

@www.route('/play/<id>/<episode>')
@www.route('/play/<id>/', defaults={'episode': None})
@www.route('/play/<id>', defaults={'episode': None})
def play(id, episode):
    source = getSetting('source')
    if request.args.get('source'): source = request.args.get('source')
    baseURL = request.base_url.split('/play')[0]

    url = f"{baseURL}/api/resolve/{id}?source={source}"
    if episode: url += f"&episode={episode}"

    resolved = requests.get(url).json()["url"]
    return render_template('play.html', preloader="/static/img/preloader/1.png", resolved=resolved)


@www.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

############### M3U ###############

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