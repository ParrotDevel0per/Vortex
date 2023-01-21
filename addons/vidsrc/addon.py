from flask import Blueprint, request, Response
from classes.plugin import Plugin
from classes.browser import Firefox
from classes.net import NET
from bs4 import BeautifulSoup
import re
import time
import base64
from utils.common import randStr
from utils.users import reqToToken
from utils.addonSettings import setAddonSetting, getAddonSetting
import json

name = "vidsrc"
vidsrcBP = Blueprint(name, __name__)
database = {}
sleepTime = 100 # Interval of updating token
expireAfter = 3 * 60 * 60 # When unused token will expire, must be bigger than sleepTime

def checkIfExpired():
    for key in database:
        if database[key]["expire"] > int(time.time()) + expireAfter:
            del database[key]

def refreshToken(token):
    r = NET().GET(token["refresher"], headers=token["headers"], useProxy=getAddonSetting(name, "useProxy").lower() == "true", usePHPProxy=getAddonSetting(name, "phpProxyEnabled").lower() == "true")
    global database
    database[token["uid"]]["expire"] = int(time.time()) + sleepTime


@vidsrcBP.route('/playlist.m3u8')
def playlist():
    wmsAuthSign = request.args.get('wmsAuthSign')
    if wmsAuthSign is None: return "Forbidden"
    wmsAuthSign = json.loads(base64.b64decode(wmsAuthSign).decode('utf-8'))
    if wmsAuthSign["uid"] not in database: return "Forbidden"
    if database[wmsAuthSign["uid"]]["expire"] < int(time.time()): refreshToken(wmsAuthSign)
    r = NET().GET(wmsAuthSign['url'], headers=wmsAuthSign["headers"], useProxy=getAddonSetting(name, "useProxy").lower() == "true", usePHPProxy=getAddonSetting(name, "phpProxyEnabled").lower() == "true")
    wmsAuthSign = base64.b64encode(json.dumps(wmsAuthSign).encode('utf-8')).decode('utf-8')
    return Response(r.text.replace("http", f"/p/{name}/ts?url=http").replace(".ts", f".ts&wmsAuthSign={wmsAuthSign}&token={reqToToken(request)}"), mimetype='application/x-mpegURL')

@vidsrcBP.route('/ts')
def ts():
    wmsAuthSign = request.args.get('wmsAuthSign')
    if wmsAuthSign is None: return "Forbidden"
    wmsAuthSign = json.loads(base64.b64decode(wmsAuthSign).decode('utf-8'))
    if wmsAuthSign["uid"] not in database: return "Forbidden"
    if database[wmsAuthSign["uid"]]["expire"] < int(time.time()): refreshToken(wmsAuthSign)
    r = NET().GET(request.args.get("url"), headers=wmsAuthSign["headers"], useProxy=getAddonSetting(name, "useProxy").lower() == "true", usePHPProxy=getAddonSetting(name, "phpProxyEnabled").lower() == "true")
    return Response(r.content, mimetype='video/mp2t')

class VidSrc(Plugin):
    def __init__(self) -> None:
        self.metadata = {
            "name": "VidSrc",
            "desc": "Plugin for grabbing streams from vidsrc.me",
            "author": "Parrot Developers",
            "id": "vidsrc",
            "logo": "logo.png",
            "resolver": {
                "name": "vidsrc",
                "func": self.resolve,
            },
            "settings": ["phpProxyEnabled", "useProxy"],
        }

        if not getAddonSetting(name, "phpProxyEnabled"):
            setAddonSetting(name, "phpProxyEnabled", "false")

        if not getAddonSetting(name, "useProxy"):
            setAddonSetting(name, "useProxy", "false")
    
    
    def resolve(self, imdbid, episode=None):
        url = "https://v2.vidsrc.me/embed/{}/".format(imdbid)
        if episode != None: url += "{}/".format(episode)

        firefox = Firefox()
        firefox.addHeader("Referer", "https://vidsrc.me/")
        r = NET().GET(url, headers=firefox.headers, useProxy=getAddonSetting(name, "useProxy").lower() == "true", usePHPProxy=getAddonSetting(name, "phpProxyEnabled").lower() == "true")
        #print(r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        iframe = soup.find('iframe', id='player_iframe')
        src = iframe['src'].replace('//', 'https://')
        firefox.addHeader("Referer", src)
        r = NET().GET(src, headers=firefox.headers, useProxy=getAddonSetting(name, "useProxy").lower() == "true", usePHPProxy=getAddonSetting(name, "phpProxyEnabled").lower() == "true")
        src = re.search(r'src: \'(.*?)\'', r.text).group(1).replace("//", "https://")
        firefox.addHeader("Referer", src)
        r = NET().GET(src, headers=firefox.headers, allow_redirects=True, useProxy=getAddonSetting(name, "useProxy").lower() == "true", usePHPProxy=getAddonSetting(name, "phpProxyEnabled").lower() == "true")
        hlsurl = re.search(r'video.setAttribute\("src" , "(.*?)"\)', r.text).group(1)
        path = re.findall(r'var path = "(.*?)"', r.text)[1].replace("//", "https://")
        firefox.reInitHeaders()
        firefox.addHeader("Referer", "https://vidsrc.stream/")

        UID = randStr(32)
        NET().GET(path, headers=firefox.headers, useProxy=getAddonSetting(name, "useProxy").lower() == "true", usePHPProxy=getAddonSetting(name, "phpProxyEnabled").lower() == "true").text # ! do not remove this line, otherwise everything gets fucked

        # create wmsAuthSign
        wmsAuthSign = {}
        wmsAuthSign["url"] = hlsurl
        wmsAuthSign["refresher"] = path
        wmsAuthSign["headers"] = firefox.headers
        wmsAuthSign["uid"] = UID
        wmsAuthSign = base64.b64encode(json.dumps(wmsAuthSign).encode('utf-8')).decode('utf-8')
        
        expire = int(time.time()) + sleepTime
        global database
        database.update({
            UID: {
                "expire": expire
            }
        })
        return f"/p/{name}/playlist.m3u8?wmsAuthSign={wmsAuthSign}&token=[[token]]"

    # Required
    def blueprint(self) -> Blueprint:
        return vidsrcBP
