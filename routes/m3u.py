from flask import Blueprint, request, redirect
from utils.settings import getSetting
from utils.paths import DB_FOLDER
from utils.users import reqToToken
from classes.net import NET
from utils.common import baseurl
import os

m3u = Blueprint("m3u", __name__)
playlistFile = os.path.join(DB_FOLDER, "playlist.json")

@m3u.route('/play/<id>.<ext>')
@m3u.route('/play/<id>', defaults={"ext": "mp4"})
def play_m3u8(id, ext):
    source = getSetting('source')
    if request.args.get('source'): source = request.args.get('source')
    try: resolved = NET().localGET(request, f"/api/resolve/{id}?source={source}").json()["url"]
    except: resolved = ""
    if "/" not in resolved: return "Error"
    if request.args.get("view") == "true":
        return resolved
    return redirect(resolved, code=302)

@m3u.route('/play/<id>/<episode>.<ext>')
@m3u.route('/play/<id>/<episode>', defaults={"ext": "mp4"})
def play_m3u8_episode(id, episode, ext):
    source = getSetting('source')
    if request.args.get('source'): source = request.args.get('source')
    try:
        resolved = NET().localGET(request, f"/api/resolve/{id}?episode={episode}&source={source}").json()["url"]
    except: resolved = ""
    if request.args.get("view") == "true":
        return resolved
    return redirect(resolved, code=302)

@m3u.route('/playlist.m3u')
def playlistm3u():
    source = getSetting('source')
    if request.args.get('source'): source = request.args.get('source')
    playlistID = request.args.get("id")
    if not playlistID:
        return "No playlistID provided"


    baseURL = baseurl(request)
    resp = NET().localGET(request, f"/api/playlist/{playlistID}").json()

    proxifyPoster = getSetting("proxifyM3UPosters")
    m3u = "#EXTM3U\n"

    auth = f"&token={reqToToken(request)}"
    if request.args.get("username") and request.args.get("password"):
        auth = f"&username={request.args.get('username')}&password={request.args.get('password')}"
    
    for i, item in resp["results"]["items"].items():
        id = item["id"]

        if item["kind"] == "movie":     
            title = f'[{item["year"]}] {item["title"]}'
            poster = item["poster"]
            if proxifyPoster:
                poster = f"{baseURL}/api/poster/{id}?do=show{auth}"
            m3u += f'#EXTINF:-1 tvg-logo="{poster}" group-title="Movies" tvg-id="{id}" tvg-name="{title}", {title}\n'
            m3u += f'{baseURL}/play/{id}?source={source}{auth}\n'
        else:
            m3u += NET().localGET(request, f"/show/{id}.m3u").text.replace("#EXTM3U\n", "")
    return m3u

@m3u.route('/show/<id>.m3u')
def showm3u(id):
    source = getSetting('source')
    if request.args.get('source'): source = request.args.get('source')
    baseURL = baseurl(request)
    resp = NET().localGET(request, f"/api/seriesToPlaylist/{id}").json()
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
            m3u += f'#EXTINF:-1 tvg-logo="{poster}" tvg-id="{id}" tvg-name="{title}" group-title="{group}", {title}\n{baseURL}/play/{id}/{season}-{episode}?source={source}{auth}\n'
    return m3u