from flask import Blueprint, request, Response
from classes.plugin import Plugin
from classes.browser import Firefox
from classes.net import NET
import re
import json
from utils.common import girc, base64encode
from utils.addonSettings import setAddonSetting, getAddonSetting
from hosts.streamlare import StreamLare
import base64

n2embed = Blueprint("2embed", __name__)

@n2embed.route('/playlist.m3u8')
def playlist():
    wmsAuthSign = request.args.get('wmsAuthSign')
    if wmsAuthSign is None:
        return "Forbidden"
    wmsAuthSign = json.loads(base64.b64decode(wmsAuthSign).decode('utf-8'))
    r = NET().GET(
        wmsAuthSign['url'], headers=wmsAuthSign["headers"],
        usePHPProxy=getAddonSetting("2embed", "phpProxyEnabled").lower() == "true",
        useProxy=getAddonSetting("2embed", "useProxy").lower() == "true"
    )
    m3u8URL = wmsAuthSign['url']
    wmsAuthSign = base64.b64encode(json.dumps(wmsAuthSign).encode('utf-8')).decode('utf-8')

    newM3U8 = []
    for line in r.text.split("\n"):
        if line.startswith("#"): newM3U8.append(line)
        if line.startswith("_") == False: continue
        newM3U8.append(m3u8URL.replace("master.m3u8", "").replace("playlist.m3u8", "") + line)
    return Response("\n".join(newM3U8), mimetype='application/x-mpegURL')

# TODO: Add ts proxy, not required for now

class toEmbed(Plugin):
    def __init__(self) -> None:
        self.metadata = {
            "name": "2embed",
            "desc": "Plugin for grabbing streams from 2embed.to",
            "author": "Parrot Developers",
            "id": "2embed",
            "logo": "logo.png",
            "resolver": {
                "name": "2embed",
                "func": self.resolve,
            },
            "settings": ["phpProxyEnabled", "useProxy"]
        }

        if not getAddonSetting("2embed", "phpProxyEnabled"):
            setAddonSetting("2embed", "phpProxyEnabled", "false")

        if not getAddonSetting("2embed", "useProxy"):
            setAddonSetting("2embed", "useProxy", "false")
    
    
    
    def resolve(self, imdbid, episode=None):
        url = f"https://www.2embed.to/embed/imdb/movie?id={imdbid}"
        if episode:
            episode = episode.split("-")
            season = episode[0]
            episode = episode[1]
            url = f"https://www.2embed.to/embed/imdb/tv?id={imdbid}&s={season}&e={episode}"

        firefox = Firefox()

        resp = NET().GET(
            url,
            headers=firefox.headers,
            usePHPProxy=getAddonSetting("2embed", "phpProxyEnabled").lower() == "true",
            useProxy=getAddonSetting("2embed", "useProxy").lower() == "true"
        )
        dataID = re.findall(
            re.compile('data-id="(.*?)">Server Streamlare</a>', flags=re.MULTILINE), resp.text
        )[0]

        token = girc(
            resp.text,
            url,
            'aHR0cHM6Ly93d3cuMmVtYmVkLnRvOjQ0Mw..', # Decoded: https://2embed.to:443
            usePHPProxy=getAddonSetting("2embed", "phpProxyEnabled").lower() == "true",
            useProxy=getAddonSetting("2embed", "useProxy").lower() == "true"
        )

        firefox.addHeader("Referer", url)
        embedurl = NET().GET(
            f"https://www.2embed.to/ajax/embed/play?id={dataID}&_token={token}", 
            headers=firefox.headers,
            usePHPProxy=getAddonSetting("2embed", "phpProxyEnabled").lower() == "true",
            useProxy=getAddonSetting("2embed", "useProxy").lower() == "true"
        ).json()["link"]
        url, headers = StreamLare().grab(
            embedurl,
            usePHPProxy=getAddonSetting("2embed", "phpProxyEnabled").lower() == "true",
            useProxy=getAddonSetting("2embed", "useProxy").lower() == "true"
        )

        if ".mp4" in url:
            return f"/api/proxy/base64:{base64encode(url)}&headers={base64encode(json.dumps(headers))}&token=[[token]]&usePHPProxy={getAddonSetting('2embed', 'phpProxyEnabled').lower() == 'true'}&useProxy={getAddonSetting('2embed', 'useProxy').lower() == 'true'}"

        # create wmsAuthSign
        wmsAuthSign = {}
        wmsAuthSign["url"] = url
        wmsAuthSign["headers"] = headers
        wmsAuthSign = base64.b64encode(json.dumps(wmsAuthSign).encode('utf-8')).decode('utf-8')
        
        return f"/p/2embed/playlist.m3u8?wmsAuthSign={wmsAuthSign}&token=[[token]]"



    # Required
    def blueprint(self) -> Blueprint:
        return n2embed
