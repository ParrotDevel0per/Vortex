from flask import Blueprint, request, redirect
from utils.settings import getSetting
from utils.paths import DB_FOLDER
from utils.users import verify, LAH, reqToToken
import requests
import json
import os

m3u = Blueprint("m3u", __name__)
playlistFile = os.path.join(DB_FOLDER, "playlist.json")

@m3u.route('/play/<id>.m3u8')
def play_m3u8(id):
    if verify(request) == False: return "Forbidden", 403

    source = getSetting('source')
    if request.args.get('source'): source = request.args.get('source')
    try: resolved = requests.get(f"{request.base_url.split('/play')[0]}/api/resolve/{id}?source={source}", headers=LAH(request)).json()["url"]
    except: resolved = ""
    return redirect(resolved, code=302)

@m3u.route('/play/<id>/<episode>.m3u8')
def play_m3u8_episode(id, episode):
    if verify(request) == False: return "Forbidden", 403

    source = getSetting('source')
    if request.args.get('source'): source = request.args.get('source')
    try: resolved = requests.get(f"{request.base_url.split('/play')[0]}/api/resolve/{id}?episode={episode}&source={source}", headers=LAH(request)).json()["url"]
    except: resolved = ""
    return redirect(resolved, code=302)

@m3u.route('/playlist.m3u')
def playlistm3u8():
    if verify(request) == False: return "Forbidden", 403

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
        if proxifyPoster: poster = f"{baseURL}/api/poster/{id}?do=show&token={reqToToken()}"
        m3u += f'#EXTINF:-1 tvg-logo="{poster}" tvg-id="{id}" tvg-name="{title}", {title}\n{baseURL}/play/{id}.m3u8?source={source}&token={reqToToken()}\n'
    return m3u

@m3u.route('/show/<id>.m3u')
def showm3u(id):
    if verify(request) == False: return "Forbidden", 403

    if not os.path.exists(playlistFile):
        return "Playlist file not found"
    source = getSetting('source')
    if request.args.get('source'): source = request.args.get('source')
    baseURL = request.base_url.split('/show')[0]
    resp = requests.get(f"{baseURL}/api/seriesToPlaylist/{id}").json()
    poster = resp["poster"]
    if getSetting("proxifyM3UPosters"):
        poster = f"{baseURL}/api/poster/{id}?do=show&token={reqToToken()}"
    m3u = "#EXTM3U\n"
    for season in resp["seasons"]:
        for episode in resp["seasons"][season]:
            title = resp["seasons"][season][episode]["title"]
            group = resp["seasons"][season][episode]["group"]
            m3u += f'#EXTINF:-1 tvg-logo="{poster}" tvg-id="{id}" tvg-name="{title}" group-title="{group}", {title}\n{baseURL}/play/{id}/{season}-{episode}.m3u8?source={source}&token={reqToToken()}\n'
    return m3u