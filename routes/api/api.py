import hashlib
from flask import Blueprint, jsonify, Response, redirect, request, send_from_directory, send_file
from utils.settings import getSetting
from classes.imdb import IMDB
from classes.fanarttv import FanartTV
from classes.cli import CLI
import base64
import json
import random
#from plugins import *
from classes.plugin import Plugin
from utils.paths import POSTER_FOLDER, BANNER_FOLDER, ADDONS_FOLDER
from utils.users import deleteUser, reqToUID, userdata, UD, changeValue, deleteUser, defaultHome, reqToToken
from utils.cache import getCachedItem, cacheItem
from classes.browser import Firefox
from classes.net import NET
from utils.addonSettings import setAddonSetting, getAddonSetting
from utils.common import chunkedDownload, sanitize, get_simple_keys, baseurl
import os
from prettytable import PrettyTable
import time
import gzip
import io
import urllib

api = Blueprint('api', __name__)

@api.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'message': 'API Running'
    })

featuredMovies = {
    "Joker": {
        "img": "/api/banner/tt7286456?do=show",
        "title": "JOKER",
        "line": "SMILE AND PUT ON A HAPPY FACE",
        "info": "8.4/10\u00A0\u00A02019\u00A0\u00A0Crime, Drama, Thriller\u00A0\u00A02h 20m",
        "plot": "A socially inept clown for hire - Arthur Fleck aspires to be a stand up comedian among his small job working dressed as a clown holding a sign for advertising. He takes care of his mother- Penny Fleck, and as he learns more about his mental illness, he learns more about his past. Dealing with all the negativity and bullying from society he heads downwards on a spiral, in turn showing how his alter ego \"Joker\", came to be.",
		"imdbID": "tt7286456",
		"kind": "movie",
    },
    "JohnWick4": {
        "img": "/api/banner/tt10366206?do=show",
        "title": "John Wick: Chapter 4",
        "line": "",
        "info": "8.5/10\u00A0\u00A02023\u00A0\u00A0Action, Crime, Thriller\u00A0\u00A02h 49m",
        "plot": "John Wick uncovers a path to defeating The High Table. But before he can earn his freedom, Wick must face off against a new enemy with powerful alliances across the globe and forces that turn old friends into foes.",
		"imdbID": "tt10366206",
		"kind": "movie",
    },
    "ScreamVI": {
        "img": "/api/banner/tt17663992?do=show",
        "title": "Scream <strong style=\"color:red;\">VI</strong>",
        "line": "",
        "info": "7.2/10\u00A0\u00A02023\u00A0\u00A0Horror, Mystery, Thriller\u00A0\u00A02h 2m",
        "plot": 'Following the latest Ghostface killings, the four survivors leave Woodsboro behind and start a fresh chapter. In Scream VI, Melissa Barrera ("Sam Carpenter"), Jasmin Savoy Brown ("Mindy Meeks-Martin"), Mason Gooding ("Chad Meeks-Martin"), Jenna Ortega ("Tara Carpenter"), Hayden Panettiere ("Kirby Reed") and Courteney Cox ("Gale Weathers") return to their roles in the franchise alongside Jack Champion, Henry Czerny, Liana Liberato, Dermot Mulroney, Devyn Nekoda, Tony Revolori, Josh Segarra, and Samara Weaving.',
		"imdbID": "tt17663992",
		"kind": "movie",
    }
}

@api.route('/featured')
def featured():
    ft = random.choice(list(featuredMovies.values()))
    ft["inFavorites"] = NET().localGET(request, f"/api/isInFavorites/{ft['imdbID'].replace('tt', '')}").json()['status'] == 'ok'
    return ft

@api.route('/homeMenu')
def homeMenu():
    return jsonify(
        userdata(reqToUID(request))['home'],
    )

@api.route('/defaultHome')
def defaultHome_():
    return defaultHome()

@api.route('/addons')
def addons_():
    plugin = Plugin()
    return plugin.plugins

@api.route('/addonLogo/<id>')
def addonLogo(id):
    plugin = Plugin()
    logo = ""
    for plugin_ in plugin.plugins:
        if plugin_["id"] != id:
            continue
        logo = plugin_["logo"]
        break
    else:
        return {"status": "error"}

    if os.path.exists(os.path.join(os.getcwd(), "addons", id, logo)):
        return send_file(os.path.join(os.getcwd(), "addons", id, logo))

    if os.path.exists(os.path.join(ADDONS_FOLDER, id ,logo)):
        return send_file(os.path.join(ADDONS_FOLDER, id ,logo))
    
    return {"status": "error"}

@api.route('/updateHomeMenu')
def updateHomeMenu():
    new = request.args.get("new")
    if not new: return "Error"
    new = base64.b64decode(new.encode()).decode()
    new = json.loads(new)
    
    changeValue(reqToUID(request), "home", new)

    return "Done"


@api.route('/addonSettings')
def addonSettings():
    id = request.args.get("id")
    do = request.args.get("do", "").lower()
    key = request.args.get("key")
    value = request.args.get("value", "")

    if do == "set":
        setAddonSetting(id, key, value)
        return "Done"
    elif do == "get":
        return getAddonSetting(id, key)
    else:
        return "Invalid key"


@api.route('/terminal')
def terminal():
    cmd = request.args.get("cmd")
    if not cmd: return "Error"
    cmd = base64.b64decode(cmd.encode()).decode()
            
    if " " in cmd: cmd = cmd.split(" ")
    else: cmd = [cmd]

    if cmd[0].lower() in ["ff", "exit"]:
        return "This command is not allowed in web terminal."

    runner = CLI()
    for item in runner.commands:
        if cmd[0] != item["name"]: continue
        cmd.pop(0)

        try:
            resp = item["run"](runner, *tuple(cmd))
            if type(resp) == PrettyTable:
                return str(resp).replace("\n", "<br/>").replace(" ", "&nbsp;")
            return resp
        except Exception as e: 
            return "Invalid command"
    return "Invalid command"


@api.route('/userInfo')
def userInfo():
    data = userdata(reqToUID(request))
    if request.args.get("all") == 'true': return data

    if 'favorites' in data: del data['favorites']
    if 'playlist' in data: del data['playlist']
    if 'history' in data: del data['history']
    if 'password' in data: del data['password']
    return data

@api.route('/users')
def users():
    resp = {}
    userdata = UD.DB()
    for k, v in userdata.items():
        user = {
            "UID": v["UID"],
            "username": v["username"],
            "isAdmin": v["isAdmin"],
            "isBanned": v["isBanned"],
            "ip": v["ip"] if getSetting("saveIPs").lower() == 'true' else "Disabled",
            "email": v["email"],
        }
        resp[k] = user
    return resp

@api.route('/promoteDemote/<uid>')
@api.route('/promoteDemote', defaults={"uid": None})
def promoteDemote(uid):
    if not uid: return jsonify({
        'status': 'error',
        'message': 'No UID Specified'
    })

    data = userdata(uid)
    if data["isAdmin"]:
        changeValue(uid, "isAdmin", False)
    else:
        changeValue(uid, "isAdmin", True)
    
    return "Done"

@api.route('/banUnban/<uid>')
@api.route('/banUnban', defaults={"uid": None})
def banUnban(uid):
    if not uid: return jsonify({
        'status': 'error',
        'message': 'No UID Specified'
    })

    data = userdata(uid)
    if data["isBanned"]:
        changeValue(uid, "isBanned", False)
    else:
        changeValue(uid, "isBanned", True)
    
    return "Done"

@api.route('/deleteUser/<uid>')
@api.route('/deleteUser', defaults={"uid": None})
def deleteUser_(uid):
    if not uid: return jsonify({
        'status': 'error',
        'message': 'No UID Specified'
    })
    deleteUser(uid)
    return "Done"

@api.route('/changePassword/<uid>/<password>')
@api.route('/changePassword', defaults={"uid": None, "password": None})
def changePassword_(uid, password):
    if not uid or not password: return jsonify({
        'status': 'error',
        'message': 'No UID or password Specified'
    })
    changeValue(
        uid,
        "password",
        hashlib.sha512(password.encode()).hexdigest()
    )
    return "Done"


@api.route("/subtitles/<id>")
def subtitles(id):
    if id.startswith("tt"): id = id[2:]

    cached = getCachedItem(f"Subtitles-{id}.json", "SubtitlesData")
    if cached == None:
        browser = Firefox()
        browser.addHeader("X-User-Agent", "trailers.to-UA")
        data = NET().GET(f"https://rest.opensubtitles.org/search/imdbid-{id}", headers=browser.headers, useProxy=False).json()
        type = data[0]["MovieKind"]
        results = {}

        if type == "movie":
            d = []
            grabbed = []
            for sub in data:
                if sub["LanguageName"] in grabbed:
                    continue
                d.append({
                    "lang": sub["LanguageName"],
                    "url": sub["SubDownloadLink"]
                })
                grabbed.append(sub["LanguageName"])
            results = {
                "results": d
            }

        else:
            for sub in data:
                if sub["SeriesSeason"] not in results:
                    results[sub["SeriesSeason"]] = {}
                
                if sub["SeriesEpisode"] not in results[sub["SeriesSeason"]]:
                    results[sub["SeriesSeason"]][sub["SeriesEpisode"]] = {}

                if sub["LanguageName"] not in results[sub["SeriesSeason"]][sub["SeriesEpisode"]]:
                    results[sub["SeriesSeason"]][sub["SeriesEpisode"]][sub["LanguageName"]] = sub["SubDownloadLink"]

            results = {
                "results": results
            }
        
        cacheItem(f"Subtitles-{id}.json", "SubtitlesData", json.dumps(results))


    return jsonify({
        "id": "tt"+id,
        "results": json.loads(getCachedItem(f"Subtitles-{id}.json", "SubtitlesData"))["results"]
    })

@api.route("/ungzip.<ext>")
def ungzip(ext):
    url = request.args.get("url")
    response = urllib.request.urlopen(url)
    compressed_file = io.BytesIO(response.read())
    decompressed_file = gzip.GzipFile(fileobj=compressed_file)
    return decompressed_file.read()


@api.route('/sources/<id>')
@api.route('/sources/', defaults={'id': None})
def sources(id):
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })

    kind = request.args.get("kind")
    if not kind: return jsonify({
        'status': 'error',
        'message': 'No Type provided'
    })

    if kind == "tv series":
        kind = "show"


    response = []

    if kind == "movie":
        for k,v in Plugin().sources.items():
            response.append({
                "name": k,
                "url": v["run"](id),
                "id": k,
            })
        return jsonify(response)

    EC = NET().localGET(request, f"/api/episodeCount/{id}").json()["results"]
    NOS = len(get_simple_keys(EC))
    
    for k,v in Plugin().sources.items():
        temp = {
            "name": k,
            "url": "",
            "id": k,
            "seasons": []
        }

        for i in range(NOS):
            i += 1
            seasonTemp = {
                "name": f"Season {i}",
                "id": f"season{i}",
                "episodes": []
            }
            for j in range(int(EC[str(i)])):
                j += 1
                seasonTemp["episodes"].append({
                    "name": f"Episode {j}",
                    "id": f"episode{i}-{j}",
                    "url": v["run"](id, f"{i}-{j}")
                })
            temp["seasons"].append(seasonTemp)
        response.append(temp)
    return jsonify(response)
            






@api.route('/poster/<id>')
@api.route('/poster/', defaults={'id': None})
def poster(id):
    if not os.path.exists(POSTER_FOLDER):
        os.makedirs(POSTER_FOLDER)
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    do = request.args.get('do', None)
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ?do provided'
    })
    baseURL = request.base_url.split('/api')[0]
    if do == 'redirect':
        p = IMDB().IMDBtoPoster(id)
        posterURL = p if p else f"{baseURL}/static/img/nopicture.jpg"
        return redirect(posterURL)

    elif do == 'show':
        listed = os.listdir(POSTER_FOLDER)

        if f"tt{id}.png" not in listed and f"tt{id}.png.gz" not in listed:
            p = IMDB().IMDBtoPoster(id)
            chunkedDownload(
                p if p else f"{baseURL}/static/img/nopicture.jpg",
                os.path.join(POSTER_FOLDER,f"tt{id}.png")
            )

            if getSetting("gzipPosters").lower() == "true":
                with gzip.open(os.path.join(POSTER_FOLDER,f"tt{id}.png.gz"), "wb") as imageGzip:
                    imageGzip.write(open(os.path.join(POSTER_FOLDER,f"tt{id}.png"), "rb").read())
                os.remove(os.path.join(POSTER_FOLDER,f"tt{id}.png"))
            listed = os.listdir(POSTER_FOLDER)

        if f"tt{id}.png" in listed:
            return send_from_directory(POSTER_FOLDER, f"tt{id}.png")

        if f"tt{id}.png.gz" in listed:
            return Response(gzip.open(os.path.join(POSTER_FOLDER,f"tt{id}.png.gz"), 'rb').read(), mimetype="image/png")
        return "Error Occurred"
 
    return "Wrong option"

@api.route('/banner/<id>')
@api.route('/banner/', defaults={'id': None})
def banner(id):
    if not os.path.exists(BANNER_FOLDER):
        os.makedirs(BANNER_FOLDER)

    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    do = request.args.get('do', None)
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ?do provided'
    })

    if do == 'redirect':
        return redirect(FanartTV().getBanner(f"tt{id}"))

    elif do == 'show':
        listed = os.listdir(BANNER_FOLDER)

        if f"tt{id}.png" not in listed and f"tt{id}.png.gz" not in listed:
            p = FanartTV().getBanner(f"tt{id}")
            if not p:
                return ""
            if "/api/poster/" in p:
                return redirect(baseurl(request)+p)

            chunkedDownload(
                p if p else f"{baseurl(request)}/static/img/nopicture.jpg",
                os.path.join(BANNER_FOLDER,f"tt{id}.png")
            )

            if getSetting("gzipBanners").lower() == "true":
                with gzip.open(os.path.join(BANNER_FOLDER,f"tt{id}.png.gz"), "wb") as imageGzip:
                    imageGzip.write(open(os.path.join(BANNER_FOLDER,f"tt{id}.png"), "rb").read())
                os.remove(os.path.join(BANNER_FOLDER,f"tt{id}.png"))
            listed = os.listdir(POSTER_FOLDER)


        if f"tt{id}.png" in listed:
            return send_from_directory(BANNER_FOLDER, f"tt{id}.png")

        if f"tt{id}.png.gz" in listed:
            return Response(gzip.open(os.path.join(BANNER_FOLDER,f"tt{id}.png.gz"), 'rb').read(), mimetype="image/png")
        return "Error Occurred"


@api.route('/search/<query>')
@api.route('/search/', defaults={'query': None})
def search(query):
    query = sanitize(query)
    if not query: return jsonify({
        'status': 'error',
        'message': 'No query provided'
    })
    cached = getCachedItem(f"search-query-{query.replace(' ', '---')}.json", "search")
    if cached == None:
        results = IMDB().search(query)
        cacheItem(f"search-query-{query.replace(' ', '---')}.json", "search", json.dumps(results))
        return jsonify({
            "query": query,
            "results": results
        })
    #print(f"Returning cached search results for \"{query}\"")
    return jsonify({
        "query": query,
        "results": json.loads(cached)
    })

@api.route('/seasons/<id>')
@api.route('/seasons/', defaults={'id': None})
def seasons(id):
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    cached = getCachedItem(f"seasons-{id}.json", "seasons")
    if cached == None:
        results = IMDB().seasons(id)
        cacheItem(f"seasons-{id}.json", "seasons", json.dumps(results))
        return jsonify({
            "id": id,
            "results": results
        })
    #print(f"Returning cached seasons for \"{id}\"")
    return jsonify({
        "id": id,
        "results": json.loads(cached)
    })

@api.route('/episodes/<id>/<season>')
@api.route('/episodes/', defaults={'id': None, 'season': None})
def episodes(id, season):
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if season == None: return jsonify({
        'status': 'error',
        'message': 'No season provided'
    })
    if id.startswith("tt"): id = id[2:]
    if not season: return jsonify({
        'status': 'error',
        'message': 'No season provided'
    })
    cached = getCachedItem(f"episodes-{id}-{season}.json", "episodes")
    if cached == None:
        results = IMDB().episodes(id, season)
        cacheItem(f"episodes-{id}-{season}.json", "episodes", json.dumps(results))
        return jsonify({
            "id": id,
            "season": season,
            "results": results
        })
    #print(f"Returning cached episodes for \"{id}\"")
    return jsonify({
        "id": id,
        "season": season,
        "results": json.loads(cached)
    })

@api.route('/episodeCount/<id>')
@api.route('/episodeCount/', defaults={'id': None})
def episodeCount(id):
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    cached = getCachedItem(f"episodeCount-{id}.json", "episodeCounts")
    if cached == None:
        results = IMDB().allEpisodesCount(id)
        cacheItem(f"episodeCount-{id}.json", "episodeCounts", json.dumps(results))
        return jsonify({
            "id": id,
            "results": results
        })
    return jsonify({
        "id": id,
        "results": json.loads(cached)
    })

@api.route('/top250movies/')
def top250movies():
    cached = getCachedItem("top250movies.json", "imdbCache")
    if cached == None:
        results = IMDB().top250movies()
        cacheItem("top250movies.json", "imdbCache", json.dumps(results))
        return jsonify({
            "results": results
        })
    #print("Returning cached top250movies.json")
    return jsonify({
        "results": json.loads(cached)
    })

@api.route('/bottom100movies/')
def bottom100movies():
    cached = getCachedItem("bottom100movies.json", "imdbCache")
    if cached == None:
        results = IMDB().bottom100movies()
        cacheItem("bottom100movies.json", "imdbCache", json.dumps(results))
        return jsonify({
            "results": results
        })
    #print("Returning cached bottom100movies.json")
    return jsonify({
        "results": json.loads(cached)
    })

@api.route('/getMoviesByGenres')
def getMoviesByGenres():
    genres = request.args.get("genres")
    MAX_RESULTS = 20
    if not genres: return jsonify({
        "status": "error"
    })
    if "|" in genres: genres = genres.split("|")
    else: genres = [genres]

    cached = getCachedItem("-".join(genres) + ".json", "genres")
    if cached == None:
        results = IMDB().getMoviesByGenres(genres)
        cacheItem("-".join(genres) + ".json", "genres", json.dumps(results))
        return jsonify({
            "results": dict(list(results.items())[:MAX_RESULTS])
        })
    return jsonify({
        "results": dict(list(json.loads(cached).items())[:MAX_RESULTS])
    })

@api.route('/proxy/<path:url>')
def proxy(url):
    if url.startswith("base64:"):
        url = base64.b64decode(url.split("base64:")[1]).decode("utf-8")

    headers = Firefox().headers
    try:
        if request.args.get("headers"): headers.update(json.loads(base64.b64decode(request.args.get("headers")).decode('utf-8')))
    except:
        pass
    

    r = NET().GET(url, headers=headers, stream=True, useProxy=request.args.get("useProxy", "").lower() == "true")
    return Response(r.iter_content(chunk_size=10*1024), content_type=r.headers['Content-Type'] if 'Content-Type' in r.headers else "")

@api.route('/getMovieInfo/<id>')
@api.route('/getMovieInfo/', defaults={'id': None})
def getMovieInfo(id):
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if id.startswith("tt"): id = id[2:]
    if id == "undefined": return "Error"
    rp = "" # response
    cached = getCachedItem(f"Item-{id}.json", "ItemInfoCache")
    if cached == None:
        movie = IMDB().getMovieInfo(id)
        resp = {}
        resp["title"] = movie.get('title', '')
        resp["plot"] = movie.get('plot outline', movie.get("plot", ["No Description was provided"])[0])
        resp["poster"] = movie.get("full-size cover url", "")
        resp["year"] = movie.get('year', '')
        resp["genres"] = ", ".join(movie['genres'][0:3]) if 'genres' in movie else 'N/A'
        resp["episodeCount"] = "0"
        resp["airDate"] = movie.get('original air date', "N/A")
        resp["budget"] = movie.get("box office", {"Budget": "N/A"}).get('Budget', "N/A")
        resp["rating"] = round(float(movie['rating']), 1) if 'rating' in movie else "N/A"

        # \u00A0 is unicode for space in JS
        resp["info"] = f"{resp['rating']}/10\u00A0{resp['year']}\u00A0{resp['genres']}\u00A0"
        
        # Add data based on if its movie / tv show
        if "number of seasons" in movie:
            resp["kind"] = "show"
            resp["NOS"] = movie["number of seasons"]
            resp["info"] += f"{resp['NOS']} Seasons"
        else: 
            resp["kind"] = "movie"
            resp["info"] += movie.get("duration", "0h 0m")

        cacheItem(f"Item-{id}.json", "ItemInfoCache", json.dumps(resp), expiry=(30*24*60*60))
        rp = resp
    else: rp = json.loads(cached)
    rp["inFavorites"] = NET().localGET(request, f"/api/isInFavorites/{id}").json()['status'] == 'ok'
    return jsonify(rp)
