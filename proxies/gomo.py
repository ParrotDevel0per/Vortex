import requests
from flask import request, url_for, Blueprint, Response
from plugins.gomo import grab
from utils.users import verify, reqToToken
import json
import base64
import re

gomo = Blueprint('gomo', __name__)

@gomo.route('/play')
def play():
    if verify(request) == False: return "Forbidden", 403

    item = request.args.get('item')
    if item is None: return "No item specified"
    url = f"https://gomo.to/movie/{item}"
    episode = request.args.get('episode')
    if episode:
        episode = episode.split("-")
        season = episode[0]
        episode = episode[1]
        if episode in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]: episode = "0" + episode
        if season in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]: season = "0" + season
        url = f"https://gomo.to/show/{item}/{season}-{episode}"
    resolved = grab(url)
    if resolved.endswith(".mp4"):
        return f"/api/proxy/{resolved}"
    token = {
        "url": resolved
    }
    token = base64.b64encode(json.dumps(token).encode('utf-8')).decode('utf-8')
    return url_for('gomo.playlist', wmsAuthSign=token, token=reqToToken(request))

@gomo.route('/playlist.m3u8')
def playlist():
    if verify(request) == False: return "Forbidden", 403

    token = request.args.get('wmsAuthSign')
    if token is None: return "Forbidden"
    token = json.loads(base64.b64decode(token).decode('utf-8'))
    resp = requests.get(token["url"]).text
    ext = "ts"
    redirectTo = 'gomo.ts'
    if ".m3u8" in resp: ext = "m3u8"; redirectTo = 'gomo.playlist'
    links = re.findall(r"https://.*?\." + ext, resp)
    for i in range(len(links)):
        token = {"url": links[i]}
        token = base64.b64encode(json.dumps(token).encode('utf-8')).decode('utf-8')
        resp = resp.replace(links[i], url_for(redirectTo, wmsAuthSign=token, token=reqToToken(request)))
    return Response(resp, mimetype='application/x-mpegURL')
        

@gomo.route('/ts')
def ts():
    if verify(request) == False: return "Forbidden", 403
    
    token = request.args.get('wmsAuthSign')
    if token is None: return "Forbidden"
    token = json.loads(base64.b64decode(token).decode('utf-8'))
    return Response(requests.get(token["url"]).content, mimetype='video/mp2t')