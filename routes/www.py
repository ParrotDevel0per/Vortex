from flask import Blueprint, request, render_template, send_from_directory, redirect
from utils.users import verify, LAH
from utils.paths import DB_FOLDER
from utils.settings import getSetting
import requests
import base64
import os

www = Blueprint('www', __name__)
playlistFile = os.path.join(DB_FOLDER, "playlist.json")

@www.route('/')
def index():
    if verify(request) == False: return redirect("/login")

    return render_template(
        'index.html',
        tab=request.args.get("tab") or "",
        id=request.args.get("id") or "",
        showG=request.args.get("showG") or "true",
        showFt=request.args.get("showFt") or "true",
    )

@www.route('/play/<id>/<episode>')
@www.route('/play/<id>/', defaults={'episode': None})
@www.route('/play/<id>', defaults={'episode': None})
def play(id, episode):
    if verify(request) == False: return redirect("/login")

    source = getSetting('source')
    if request.args.get('source'): source = request.args.get('source')

    baseURL = request.base_url.split('/play')[0]

    sourcesURL = "/api/sources/" + id

    sec, ep, se, epc = ("0" * 4)
    if episode:
        ep = episode.split("-")[1] # Episode
        se = episode.split("-")[0] # Season
        resp = requests.get(f"{baseURL}/api/episodeCount/{id}", headers=LAH(request)).json()
        epc = resp["results"][se] # Episode Count
        sec = len(resp["results"]) # Season Count
        sourcesURL += f"?type=show&default{source}&ep={episode}"
    else: sourcesURL += f"?type=movie"

    return render_template('play.html', ep=ep, id=id, se=se, epc=epc, sec=sec, sourcesURL=base64.b64encode(sourcesURL.encode()).decode())


@www.route('/static/<path:path>')
def send_static(path):
    if "svelte" in path: 
        if verify(request) == False:
            return "Forbidden", 403

    return send_from_directory('static', path)

