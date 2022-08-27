import requests
from flask import request, url_for, Blueprint, Response
from plugins.r2embed import grab
from utils.beautify import BeautifyM3U8
import json
import base64

r2embed = Blueprint('r2embed', __name__)

@r2embed.route('/play')
def play():
    item = request.args.get('item')
    if item is None: return "No item specified"
    url = f"https://2embed.biz/play/movie.php?imdb={item}"
    episode = request.args.get('episode')
    if episode:
        episode = episode.split("-")
        url = f"https://2embed.biz/play/series.php?imdb={item}&sea={episode[0]}&epi={episode[1]}"
    resolved, headers = grab(url)
    token = {
        "url": resolved,
        "headers": headers
    }
    token = base64.b64encode(json.dumps(token).encode('utf-8')).decode('utf-8')
    return url_for('r2embed.playlist', token=token)

@r2embed.route('/playlist.m3u8')
def playlist():
    token = request.args.get('token')
    if token is None: return "Forbidden"
    token = json.loads(base64.b64decode(token).decode('utf-8'))
    beautiful = BeautifyM3U8().beautify(url=token["url"], headers=token['headers'], proxyServer="/proxy/2embed/")
    return Response(beautiful, mimetype='application/x-mpegURL')
        

@r2embed.route('/chunk.ts')
def ts():
    token = request.args.get('token')
    if token is None: return "Forbidden"
    token = json.loads(base64.b64decode(token).decode('utf-8'))
    return Response(requests.get(token["url"], headers=token["headers"]).content, mimetype='video/mp2t')