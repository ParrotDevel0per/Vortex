import requests
from flask import request, url_for, Blueprint, Response
from plugins.vidembed import resolveVidembed
from resolvers.sbplay import sbplay
from plugins.gdriveplayer import resolveGDrivePlayer
from utils.users import verify, reqToToken
import json
import base64
import re

vidembed = Blueprint('vidembed', __name__)

@vidembed.route('/play')
def play():
    if verify(request) == False: return "Forbidden", 403

    item = request.args.get('item')
    if item is None: return "No item specified"
    url = f"https://database.gdriveplayer.us/player.php?imdb={item}"
    episode = request.args.get('episode')
    if episode:
        episode = episode.split("-")
        url = f"https://series.databasegdriveplayer.co/player.php?type=series&imdb={item}&season={episode[0]}&episode={episode[1]}"
    resolved, headers = sbplay(resolveVidembed(resolveGDrivePlayer(url), 'StreamSB').split("?")[0])
    token = {
        "url": resolved,
        "headers": headers
    }
    token = base64.b64encode(json.dumps(token).encode('utf-8')).decode('utf-8')
    return url_for('vidembed.playlist', wmsAuthSign=token, token=reqToToken(request))

@vidembed.route('/playlist.m3u8')
def playlist():
    if verify(request) == False: return "Forbidden", 403

    token = request.args.get('wmsAuthSign')
    if token is None: return "Forbidden"
    token = json.loads(base64.b64decode(token).decode('utf-8'))
    headers = token['headers']
    resp = requests.get(token["url"], headers=headers).text
    redirectTo = 'vidembed.ts'
    if ".m3u8" in resp: redirectTo = 'vidembed.playlist'
    links = re.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", resp)
    for i in range(len(links)):
        token = {
            "url": links[i],
            "headers": headers
        }
        token = base64.b64encode(json.dumps(token).encode('utf-8')).decode('utf-8')
        resp = resp.replace(links[i], url_for(redirectTo, wmsAuthSign=token, token=reqToToken(request)))
    return Response(resp, mimetype='application/x-mpegURL')
        

@vidembed.route('/ts')
def ts():
    if verify(request) == False: return "Forbidden", 403

    token = request.args.get('wmsAuthSign')
    if token is None: return "Forbidden"
    token = json.loads(base64.b64decode(token).decode('utf-8'))
    return Response(requests.get(token["url"], headers=token["headers"]).content, mimetype='video/mp2t')