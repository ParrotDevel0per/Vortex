from flask import Blueprint, request, render_template, send_from_directory
from utils.paths import DB_FOLDER
from classes.plugin import Plugin
from classes.net import NET
import os
import json

www = Blueprint('www', __name__)
playlistFile = os.path.join(DB_FOLDER, "playlist.json")

@www.route('/')
def index():
    return render_template(
        'index.html',
        tab=request.args.get("tab") or "",
        id=request.args.get("id") or "",
        showG=request.args.get("showG") or "true",
        showFt=request.args.get("showFt") or "true",
    )

@www.route('/watch/<id>/')
@www.route('/watch/<id>')
def watch(id):
    sourcesURL = f"/api/sources/{id}"
    if request.args.get('kind'): sourcesURL += f"?kind={request.args.get('kind')}"
    if request.args.get('source'): sourcesURL += f"&source={request.args.get('source')}"
    sources = NET().localGET(request, sourcesURL).json()
    return render_template('play.html', id=id, sources=json.dumps(sources), sourcesURL=sourcesURL)


@www.route("/p")
def p(): # Plugins
    return render_template("plugins.html", plugins=Plugin().plugins)

@www.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

