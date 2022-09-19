from flask import request, Blueprint
from resolvers.mixdrop import mixdrop
from resolvers.streamtape import streamtape
from plugins.csfd import translateItemToCzech
from plugins.kukajto import search, grab
from utils.users import verify, reqToToken
import difflib
import base64
import json

kukajto = Blueprint('kukajto', __name__)

@kukajto.route('/play')
def play():
    if verify(request) == False: return "Forbidden", 403

    item = request.args.get('item')
    if item is None: return "No item specified"
    episode = request.args.get('episode')
    isMovie = episode is None
    translatedTitle = translateItemToCzech(item, isMovie)
    results = search(translatedTitle)
    data = {
        "titles": [],
        "slugs": [],
    }
    for result in results:
        if isMovie and result['t'] == 'movie':
            data['titles'].append(result['name'])
            data['slugs'].append(result['slug'])
        elif not isMovie and result['t'] == 'show':
            data['titles'].append(result['name'])
            data['slugs'].append(result['slug'])
    if len(data['titles']) == 0: return "No results found"
    bestMatch = difflib.get_close_matches(translatedTitle, data['titles'], n=1, cutoff=0.5)[0]
    index = data['titles'].index(bestMatch)
    id = data['slugs'][index]
    url = f"https://film.kukaj.io/{id}"
    if not isMovie:
        episode = episode.split("-")
        season = episode[0]
        episode = episode[1]
        if len(episode) == 1: episode = "0" + episode
        if len(season) == 1: season = "0" + season
        url = f"https://serial.kukaj.io/{id}/S{season}E{episode}"
    resolved = grab(url)
    headers = None
    if "mixdrop" in resolved: resolved, headers = mixdrop(resolved, "https://kukaj.io/", mxr=True)
    else: resolved, headers = streamtape(resolved, "https://kukaj.io/")
    if not resolved: return "Failed to resolve"
    resp = f"/api/proxy/base64:{base64.b64encode(resolved.encode('utf-8')).decode('utf-8')}"
    if headers: resp += f"?headers={base64.b64encode(json.dumps(headers).encode('utf-8')).decode('utf-8')}&token={reqToToken(request)}"
    else: resp += f"?token={reqToToken(request)}"
    return resp