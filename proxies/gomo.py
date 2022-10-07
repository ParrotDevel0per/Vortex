import requests
from flask import request, url_for, Blueprint, Response
from plugins.gomo import grab
from utils.users import reqToToken
import json
import base64
import re

gomo = Blueprint('gomo', __name__)

@gomo.route('/play')
def play():
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
        return f"/api/proxy/{resolved}?token=" + reqToToken(request)
    wmsAuthSign = {
        "url": resolved
    }
    wmsAuthSign = base64.b64encode(json.dumps(wmsAuthSign).encode('utf-8')).decode('utf-8')
    return url_for('gomo.playlist', wmsAuthSign=wmsAuthSign, token=reqToToken(request))

@gomo.route('/playlist.m3u8')
def playlist():
    wmsAuthSign = request.args.get('wmsAuthSign')
    if wmsAuthSign is None: return "Forbidden"
    wmsAuthSign = json.loads(base64.b64decode(wmsAuthSign).decode('utf-8'))
    resp = requests.get(wmsAuthSign["url"]).text
    ext = "ts"
    redirectTo = 'gomo.ts'
    if ".m3u8" in resp: ext = "m3u8"; redirectTo = 'gomo.playlist'
    links = re.findall(r"https://.*?\." + ext, resp)
    for i in range(len(links)):
        wmsAuthSign = {"url": links[i]}
        wmsAuthSign = base64.b64encode(json.dumps(wmsAuthSign).encode('utf-8')).decode('utf-8')
        resp = resp.replace(links[i], url_for(redirectTo, wmsAuthSign=wmsAuthSign, token=reqToToken(request)))
    return Response(resp, mimetype='application/x-mpegURL')
        

@gomo.route('/ts')
def ts():
    wmsAuthSign = request.args.get('wmsAuthSign')
    if wmsAuthSign is None: return "Forbidden"
    wmsAuthSign = json.loads(base64.b64decode(wmsAuthSign).decode('utf-8'))
    return Response(requests.get(wmsAuthSign["url"]).content, mimetype='video/mp2t')