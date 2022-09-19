# Settings:
sleepTime = 100 # Interval of updating token
expireAfter = 3 * 60 * 60 # When unused token will expire, must be bigger than sleepTime


import requests
from flask import request, url_for, Blueprint, Response
from plugins.vidsrc import grab
from utils.users import verify, reqToToken
import json
import time
import base64
from utils.common import randStr

vidsrc = Blueprint('vidsrc', __name__)
database = {}

def getIP(request):
    xff = request.headers.get('X-Forwarded-For')
    if xff is not None: return xff
    return request.remote_addr

def checkIfExpired():
    for key in database:
        if database[key]["expire"] > int(time.time()) + expireAfter:
            del database[key]

def refreshToken(token):
    r = requests.get(token["refresher"], headers=token["headers"])
    global database
    database[token["uid"]]["expire"] = int(time.time()) + sleepTime

@vidsrc.route('/play')
def play():
    if verify(request) == False: return "Forbidden", 403

    checkIfExpired()
    item = request.args.get('item')
    if item is None: return "No item specified"
    episode = request.args.get('episode')
    url = "https://vidsrc.me/embed/{}/".format(item)
    if episode != None: url += "{}/".format(episode)
    hlsurl, refresher, headers = grab(url)
    UID = randStr(32)
    requests.get(refresher, headers=headers).text # ! do not remove this line, otherwise everything gets fucked

    # create token
    token = {}
    token["url"] = hlsurl
    token["refresher"] = refresher
    token["headers"] = headers
    token["uid"] = UID
    token = base64.b64encode(json.dumps(token).encode('utf-8')).decode('utf-8')
    
    expire = int(time.time()) + sleepTime
    global database
    database.update({
        UID: {
            "expire": expire,
            "ip": getIP(request)
        }
    })
    return url_for('vidsrc.playlist', wmsAuthSign=token)

@vidsrc.route('/playlist.m3u8')
def playlist():
    if verify(request) == False: return "Forbidden", 403

    token = request.args.get('wmsAuthSign')
    if token is None: return "Forbidden"
    token = json.loads(base64.b64decode(token).decode('utf-8'))
    if token["uid"] not in database: return "Forbidden"
    if database[token["uid"]]["expire"] < int(time.time()): refreshToken(token)
    r = requests.get(token['url'], headers=token["headers"])
    token = base64.b64encode(json.dumps(token).encode('utf-8')).decode('utf-8')
    return Response(r.text.replace("http", f"/proxy/vidsrc/ts?url=http").replace(".ts", f".ts&wmsAuthSign={token}&token={reqToToken(request)}"), mimetype='application/x-mpegURL')

@vidsrc.route('/ts')
def ts():
    if verify(request) == False: return "Forbidden", 403

    token = request.args.get('wmsAuthSign')
    if token is None: return "Forbidden"
    token = json.loads(base64.b64decode(token).decode('utf-8'))
    if token["uid"] not in database: return "Forbidden"
    if database[token["uid"]]["expire"] < int(time.time()): refreshToken(token)
    r = requests.get(request.args.get("url"), headers=token["headers"])
    return Response(r.content, mimetype='video/mp2t')