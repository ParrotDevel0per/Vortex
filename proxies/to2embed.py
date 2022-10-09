import requests
from flask import request, url_for, Blueprint, Response
from plugins.to2embed import grab
from utils.users import reqToToken
from resolvers.streamlare import streamlare
import json
import base64
import re

to2embed = Blueprint('to2embed', __name__)

@to2embed.route('/play')
def play():
    item = request.args.get('item')
    if item is None: return "No item specified"
    url = f"https://www.2embed.to/embed/imdb/movie?id={item}"
    episode = request.args.get('episode')
    if episode:
        episode = episode.split("-")
        season = episode[0]
        episode = episode[1]
        url = f"https://www.2embed.to/embed/imdb/tv?id={item}&s={season}&e={episode}"
    resolved, headers = streamlare(grab(url))
    if ".mp4" in resolved:
        return f"/api/proxy/base64:{base64.b64encode(resolved.encode()).decode()}?token={reqToToken(request)}&headers={base64.b64encode(json.dumps(headers).encode('utf-8')).decode('utf-8')}&token={reqToToken(request)}"
    wmsAuthSign = {
        "url": resolved,
        "headers": headers
    }
    wmsAuthSign = base64.b64encode(json.dumps(wmsAuthSign).encode('utf-8')).decode('utf-8')
    return url_for('to2embed.playlist', wmsAuthSign=wmsAuthSign, token=reqToToken(request))

@to2embed.route('/playlist.m3u8')
def playlist():
    wmsAuthSign = request.args.get('wmsAuthSign')
    if wmsAuthSign is None: return "Forbidden"
    wmsAuthSign = json.loads(base64.b64decode(wmsAuthSign).decode('utf-8'))
    resp = requests.get(wmsAuthSign["url"], headers=wmsAuthSign["headers"]).text
    ext = "ts"
    redirectTo = 'to2embed.ts'
    if ".m3u8" in resp: ext = "m3u8"; redirectTo = 'to2embed.playlist'
    links = re.findall(r"https://.*?\." + ext, resp)
    for i in range(len(links)):
        wmsAuthSign = {"url": links[i]}
        wmsAuthSign = base64.b64encode(json.dumps(wmsAuthSign).encode('utf-8')).decode('utf-8')
        resp = resp.replace(links[i], url_for(redirectTo, wmsAuthSign=wmsAuthSign, token=reqToToken(request)))
    return Response(resp, mimetype='application/x-mpegURL')
        

@to2embed.route('/ts')
def ts():
    wmsAuthSign = request.args.get('wmsAuthSign')
    if wmsAuthSign is None: return "Forbidden"
    wmsAuthSign = json.loads(base64.b64decode(wmsAuthSign).decode('utf-8'))
    return Response(requests.get(wmsAuthSign["url"], headers=wmsAuthSign["headers"]).content, mimetype='video/mp2t')