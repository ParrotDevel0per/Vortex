from flask import Blueprint, request, url_for, Response
from utils.beautify import BeautifyM3U8
import requests
import base64
import json
import Resolver

universal = Blueprint('universal', __name__)
beautifier = BeautifyM3U8()

@universal.route('/openConnection')
def openConnection():
    resolved = Resolver.resolve(
        request.args.get("module"),
        request.args.get('item'),
        request.args.get("episode")
    )
    if resolved.url == "":
        return url_for(
            "api.proxy",
            url="base64:"+base64.b64encode("https://google.com".encode()).decode(),
            headers={}
        )

    if ".mp4" in resolved.url:
        return url_for(
            "api.proxy",
            url="base64:"+base64.b64encode(resolved.url.encode()).decode(),
            headers=base64.b64encode(json.dumps(resolved.headers).encode()).decode()
        )

    token = {}
    token["url"] = resolved.url
    token["headers"] = resolved.headers
    token = base64.b64encode(json.dumps(token).encode('utf-8'))
    return url_for('universal.proxy', token=token.decode('utf-8'))

@universal.route('/playlist.m3u8')
def proxy():
    token = request.args.get('token')
    token = json.loads(base64.b64decode(token).decode('utf-8'))
    url = token['url']
    headers = token['headers']
    resp = requests.get(url, headers=headers)
    if not url: return Response('', status=400)

    # Get different repsonse based on file type
    resp2 = Response(resp.content)
    if ".m3u8" in resp.url or "m3u" in resp.text.lower():
        resp2 = Response(beautifier.beautify(resp.url, headers, proxyServer="/proxy/universal/").encode('utf-8'))
    
    resp2.headers['Content-Disposition'] = 'attachment; filename="playlist.m3u8"'
    resp2.headers['Content-Type'] = 'application/vnd.apple.mpegurl'
    return resp2

@universal.route('/chunk.ts')
def proxyChunk():
    token = request.args.get('token')
    token = json.loads(base64.b64decode(token).decode('utf-8'))
    url = token['url']
    headers = token['headers']
    resp = requests.get(url, headers=headers)
    resp2 = Response(resp.content)
    resp2.headers['Content-Disposition'] = 'attachment; filename="chunk.ts"'
    resp2.headers['Content-Type'] = 'video/MP2T'
    return resp2