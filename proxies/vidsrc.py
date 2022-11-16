# Settings:
sleepTime = 100 # Interval of updating token
expireAfter = 3 * 60 * 60 # When unused token will expire, must be bigger than sleepTime


from flask import request, url_for, Blueprint, Response
from utils.users import reqToToken
import json
import time
import base64
from utils.common import randStr
import Resolver
from classes.net import NET

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
    r = NET().GET(token["refresher"], headers=token["headers"])
    global database
    database[token["uid"]]["expire"] = int(time.time()) + sleepTime

@vidsrc.route('/play')
def play():
    checkIfExpired()
    item = request.args.get('item')
    if item is None: return "No item specified"
    episode = request.args.get('episode')
    
    resolved = Resolver.resolve("VidSrc", item, episode)
    hlsurl = resolved.url
    headers = resolved.headers
    refresher = resolved.refresher["url"]

    UID = randStr(32)
    NET().GET(refresher, headers=headers).text # ! do not remove this line, otherwise everything gets fucked

    # create wmsAuthSign
    wmsAuthSign = {}
    wmsAuthSign["url"] = hlsurl
    wmsAuthSign["refresher"] = refresher
    wmsAuthSign["headers"] = headers
    wmsAuthSign["uid"] = UID
    wmsAuthSign = base64.b64encode(json.dumps(wmsAuthSign).encode('utf-8')).decode('utf-8')
    
    expire = int(time.time()) + sleepTime
    global database
    database.update({
        UID: {
            "expire": expire,
            "ip": getIP(request)
        }
    })
    return url_for('vidsrc.playlist', wmsAuthSign=wmsAuthSign, token=reqToToken(request))

@vidsrc.route('/playlist.m3u8')
def playlist():
    wmsAuthSign = request.args.get('wmsAuthSign')
    if wmsAuthSign is None: return "Forbidden"
    wmsAuthSign = json.loads(base64.b64decode(wmsAuthSign).decode('utf-8'))
    if wmsAuthSign["uid"] not in database: return "Forbidden"
    if database[wmsAuthSign["uid"]]["expire"] < int(time.time()): refreshToken(wmsAuthSign)
    r = NET().GET(wmsAuthSign['url'], headers=wmsAuthSign["headers"])
    wmsAuthSign = base64.b64encode(json.dumps(wmsAuthSign).encode('utf-8')).decode('utf-8')
    return Response(r.text.replace("http", f"/proxy/vidsrc/ts?url=http").replace(".ts", f".ts&wmsAuthSign={wmsAuthSign}&token={reqToToken(request)}"), mimetype='application/x-mpegURL')

@vidsrc.route('/ts')
def ts():
    wmsAuthSign = request.args.get('wmsAuthSign')
    if wmsAuthSign is None: return "Forbidden"
    wmsAuthSign = json.loads(base64.b64decode(wmsAuthSign).decode('utf-8'))
    if wmsAuthSign["uid"] not in database: return "Forbidden"
    if database[wmsAuthSign["uid"]]["expire"] < int(time.time()): refreshToken(wmsAuthSign)
    r = NET().GET(request.args.get("url"), headers=wmsAuthSign["headers"])
    return Response(r.content, mimetype='video/mp2t')