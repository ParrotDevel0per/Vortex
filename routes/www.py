from flask import Blueprint, request, render_template, send_from_directory, url_for
from utils.paths import DB_FOLDER
from classes.net import NET
from urllib.parse import quote
import os
import json

www = Blueprint('www', __name__)
playlistFile = os.path.join(DB_FOLDER, "playlist.json")

@www.route('/')
def index():
    tab = request.args.get("tab") or ""
    id = request.args.get("id") or ""
    name, desc, image, url = "", "", "", ""
    metaTags = []

    if tab == "":
        name = "Vortex"
        desc = "Self-Hosted version of vortex"
        image = url_for("www.send_static", path="img/screenshots/Vortex-Home.png", _external=True)
        url = url_for("www.index", _external=True)

    elif tab == "search":
        name = "Vortex | Search"
        desc = "Search Movies on vortex"
        image = url_for("www.send_static", path="img/screenshots/Vortex-Search.png", _external=True)
        url = url_for("www.index", _external=True) + "?tab=playlist"

    elif tab == "favorites":
        name = "Vortex | Favorites"
        desc = "My favorites"
        image = url_for("www.send_static", path="img/screenshots/Vortex-Favorites.png", _external=True)
        url = url_for("www.index", _external=True) + '?tab=favorites'

    elif tab == "playlists":
        name = "Vortex | Playlists"
        desc = "My Playlists"
        image = url_for("www.send_static", path="img/screenshots/Vortex-Playlists.png", _external=True)
        url = url_for("www.index", _external=True) + '?tab=playlists'

    elif tab == "playlist":
        playlistData = NET().localGET(request, f"/api/playlist/{id}").json()["results"]
        name = f"Vortex | {playlistData['title']} Playlist"
        desc = f"{playlistData['title']} Playlist contains {playlistData['count']}items"
        image = f"https://corsproxy.io/?{quote(playlistData['logo'])}"
        url = url_for("www.index", _external=True) + '?tab=playlist&id=' + id

    elif tab == "addons":
        name = "Vortex | Addons"
        desc = "Installed Addons"
        image = url_for("www.send_static", path="img/screenshots/Vortex-Addons.png", _external=True)
        url = url_for("www.index", _external=True) + '?tab=addons'

    elif tab == "settings":
        name = "Vortex | Settings"
        desc = "Vortex account settings"
        image = url_for("www.send_static", path="img/screenshots/Vortex-Settings.png", _external=True)
        url = url_for("www.index", _external=True) + '?tab=settings'

    elif tab == "player":
        name = "Vortex | Player"
        desc = "Vortex Player"
        image = url_for("www.send_static", path="img/screenshots/Vortex-Player.png", _external=True)
        url = url_for("www.index", _external=True) + '?tab=player'

    metaTags.append(f'    <title>{name}</title>')
    metaTags.append(f'    <meta name="description" content="{desc}">')
    metaTags.append(f'    <meta name="theme-color" content="#0000ff">')
    metaTags.append(f'    <meta property="og:type" content="website">')
    metaTags.append(f'    <meta property="og:url" content="{url}">')
    metaTags.append(f'    <meta property="og:title" content="{name}">')
    metaTags.append(f'    <meta property="og:description" content="{desc}">')
    metaTags.append(f'    <meta property="og:image" content="{image}">')
    metaTags.append(f'    <meta property="twitter:card" content="summary_large_image">')
    metaTags.append(f'    <meta property="twitter:url" content="{url}">')
    metaTags.append(f'    <meta property="twitter:title" content="{name}">')
    metaTags.append(f'    <meta property="twitter:description" content="{desc}">')
    metaTags.append(f'    <meta property="twitter:image" content="{image}">')


    return render_template(
        'index.html',
        metaTags="\n".join(metaTags)
    )

@www.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

