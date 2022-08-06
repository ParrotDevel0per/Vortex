import requests
from flask import request, url_for, Blueprint
from plugins.gomo import grab
import json
import base64
import re

gomo = Blueprint('gomo', __name__)

@gomo.route('/play')
def play():
    item = request.args.get('item')
    if item is None: return "No item specified"
    resolved = grab(f"https://gomo.to/movie/{item}")
    if resolved.endswith(".mp4"):
        return f"/api/proxy/{resolved}"
    token = {
        "url": resolved
    }
    token = base64.b64encode(json.dumps(token).encode('utf-8')).decode('utf-8')
    return url_for('gomo.playlist', wmsAuthSign=token)

@gomo.route('/playlist.m3u8')
def playlist():
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
        resp = resp.replace(links[i], url_for(redirectTo, wmsAuthSign=token))
    return resp
        

@gomo.route('/ts')
def ts():
    token = request.args.get('wmsAuthSign')
    if token is None: return "Forbidden"
    token = json.loads(base64.b64decode(token).decode('utf-8'))
    return requests.get(token["url"]).content