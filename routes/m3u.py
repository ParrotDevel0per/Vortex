from flask import Blueprint, request, redirect
from utils.settings import getSetting
from utils.paths import DB_FOLDER
from utils.users import LAH, reqToToken
import requests
import os

m3u = Blueprint("m3u", __name__)
playlistFile = os.path.join(DB_FOLDER, "playlist.json")

@m3u.route('/play/<id>.m3u8')
def play_m3u8(id):
    source = getSetting('source')
    if request.args.get('source'): source = request.args.get('source')
    try: resolved = requests.get(f"{request.base_url.split('/play')[0]}/api/resolve/{id}?source={source}", headers=LAH(request)).json()["url"]
    except: resolved = ""
    if "/" not in resolved: return "Error"
    return redirect(resolved, code=302)

@m3u.route('/play/<id>/<episode>.m3u8')
def play_m3u8_episode(id, episode):
    source = getSetting('source')
    if request.args.get('source'): source = request.args.get('source')
    try: resolved = requests.get(f"{request.base_url.split('/play')[0]}/api/resolve/{id}?episode={episode}&source={source}", headers=LAH(request)).json()["url"]
    except: resolved = ""
    return redirect(resolved, code=302)

@m3u.route('/playlist.m3u')
def playlistm3u8():
    source = getSetting('source')
    if request.args.get('source'): source = request.args.get('source')
    baseURL = request.base_url.split('/playlist')[0]
    j = requests.get(f"{baseURL}/api/playlist/", headers=LAH(request)).json()['results']
    proxifyPoster = getSetting("proxifyM3UPosters")
    m3u = "#EXTM3U\n"

    auth = f"&token={reqToToken(request)}"
    if request.args.get("username") and request.args.get("password"):
        auth = f"&username={request.args.get('username')}&password={request.args.get('password')}"
    
    for i in j:
        title = f'[{j[i]["year"]}] {j[i]["title"]}'
        id = j[i]["id"]
        poster = j[i]["poster"]
        if proxifyPoster: poster = f"{baseURL}/api/poster/{id}?do=show{auth}"
        m3u += f'#EXTINF:-1 tvg-logo="{poster}" tvg-id="{id}" tvg-name="{title}", {title}\n{baseURL}/play/{id}.m3u8?source={source}{auth}\n'
    return m3u

@m3u.route('/show/<id>.m3u')
def showm3u(id):
    source = getSetting('source')
    if request.args.get('source'): source = request.args.get('source')
    baseURL = request.base_url.split('/show')[0]
    resp = requests.get(f"{baseURL}/api/seriesToPlaylist/{id}", headers=LAH(request)).json()
    poster = resp["poster"]
    m3u = "#EXTM3U\n"

    auth = f"&token={reqToToken(request)}"
    if request.args.get("username") and request.args.get("password"):
        auth = f"&username={request.args.get('username')}&password={request.args.get('password')}"
    
    if getSetting("proxifyM3UPosters"):
        poster = f"{baseURL}/api/poster/{id}?do=show" + auth
    
    for season in resp["seasons"]:
        for episode in resp["seasons"][season]:
            title = resp["seasons"][season][episode]["title"]
            group = resp["seasons"][season][episode]["group"]
            m3u += f'#EXTINF:-1 tvg-logo="{poster}" tvg-id="{id}" tvg-name="{title}" group-title="{group}", {title}\n{baseURL}/play/{id}/{season}-{episode}.m3u8?source={source}{auth}\n'
    return m3u