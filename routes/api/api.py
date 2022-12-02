import hashlib
from flask import Blueprint, jsonify, Response, redirect, request, send_from_directory
from utils.settings import getSetting
from classes.imdb import IMDB
from classes.fanarttv import FanartTV
from classes.cli import CLI
import requests
import base64
import json
import random
from utils.paths import POSTER_FOLDER, BANNER_FOLDER
from utils.users import deleteUser, reqToUID, LAH, userdata, UD, changeValue, deleteUser, defaultHome
from utils.cache import getCachedItem, cacheItem
from classes.browser import Firefox
from classes.net import NET
from utils.common import chunkedDownload, sanitize, get_simple_keys
import os
from prettytable import PrettyTable
import time

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
    }
}

@api.route('/featured')
def featured():
    ft = random.choice(list(featuredMovies.values()))
    ft["inFavorites"] = requests.get(request.base_url.split("/api")[0] + "/api/isInFavorites/" + ft["imdbID"].replace("tt", ""), headers=LAH(request)).json()['status'] == 'ok'
    ft["inPlaylist"] = requests.get(request.base_url.split("/api")[0] + "/api/isInPlaylist/" + ft["imdbID"].replace("tt", ""), headers=LAH(request)).json()['status'] == 'ok'
    return ft

@api.route('/homeMenu')
def homeMenu():
    return jsonify(
        userdata(reqToUID(request))['home'],
    )

@api.route('/defaultHome')
def defaultHome_():
    return defaultHome()

@api.route('/requestsIP')
def requestsIP():
    return NET().GET("https://api.my-ip.io/ip").text

@api.route('/updateHomeMenu')
def updateHomeMenu():
    new = request.args.get("new")
    if not new: return "Error"
    new = base64.b64decode(new.encode()).decode()
    new = json.loads(new)
    
    changeValue(reqToUID(request), "home", new)

    return "Done"

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


@api.route('/resolve/<id>')
@api.route('/resolve/', defaults={'id': None})
def resolve(id):
    if not id: return jsonify({
        'status': 'error',
        'message': 'No ID provided'
    })
    if not id.startswith("tt"): id = f"tt{id}"

    sources = []
    for file in os.listdir("Resolver/plugins"):
        if file.startswith("__"): continue
        sources.append(file.split(".")[0])

    use = sources[0]
    if getSetting("source") in sources:       use = getSetting("source")
    if request.args.get("source") in sources: use = request.args.get("source")

    episode = str(request.args.get("episode") or "")
    baseURL = request.base_url.split("/api")[0]
    url = ""
    if "vidsrc" in use.lower():
        url = f"{baseURL}/proxy/vidsrc/play?item={id}"
    else:
        url = f"{baseURL}/proxy/universal/openConnection?module={use}&item={id}"
    if episode: url += f"&episode={episode}"
    return jsonify({
        "id": id,
        "url": requests.get(url, headers=LAH(request)).text
    })

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


    sources = []
    for file in os.listdir("Resolver/plugins"):
        if file.startswith("__"): continue
        sources.append(file.split(".")[0])

    default = sources[0]
    if getSetting("source") in sources:       default = getSetting("source")
    if request.args.get("source") in sources: default = request.args.get("source")
    
    sources.insert(0, sources.pop(sources.index(default)))

    now = str(time.time()).split(".")[0]

    extensions = {
        "vidsrc": "m3u8",
        "kukajto": "mp4",
        "n2embed": "mp4"
    }

    baseURL = request.base_url.split("/api")[0]
    response = []

    if kind == "show":
        EC = requests.get(f"{baseURL}/api/episodeCount/{id}", headers=LAH(request)).json()["results"]
        NOS = len(get_simple_keys(EC))

        for i in range(NOS):
            i += 1

            episodes = []
            for j in range(int(EC[str(i)])):
                j += 1

                sources_ = []
                for src in sources:
                    file = f"/play/{id}/{i}-{j}.ext?source={src}&generated={now}"
                    if src in extensions: file = file.replace("ext", extensions[src])
                    else: file = file.replace(".ext", "")

                    sources_.append({
                        "title": src.replace("n2embed", "2embed"),
                        "file": file
                    })

                episodes.append({
                    "title": f"Episode {j}",
                    "folder": sources_
                })

            response.append({
                "title": f"Season {i}",
                "folder": episodes
            })
        return response

    for src in sources:
        j = {"title": src.replace("n2embed", "2embed") }
        j["file"] = f"/play/{id}.ext"
        j["file"] += f"?source={src}&generated={now}"
        j["file"] = j["file"].replace("ext", extensions[src]) if src in extensions else j["file"]
        response.append(j)
    return response



@api.route('/poster/<id>')
@api.route('/poster/', defaults={'id': None})
def poster(id):
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
        if not os.path.exists(POSTER_FOLDER): os.makedirs(POSTER_FOLDER)
        if f"tt{id}.png" not in os.listdir(POSTER_FOLDER):
            p = IMDB().IMDBtoPoster(id)
            chunkedDownload(p if p else f"{baseURL}/static/img/nopicture.jpg", os.path.join(POSTER_FOLDER, f"tt{id}.png"))
        return send_from_directory(POSTER_FOLDER, f"tt{id}.png")

@api.route('/banner/<id>')
@api.route('/banner/', defaults={'id': None})
def banner(id):
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
        if not os.path.exists(BANNER_FOLDER): os.makedirs(BANNER_FOLDER)
        if f"tt{id}.png" not in os.listdir(BANNER_FOLDER):
            url = FanartTV().getBanner(f"tt{id}")
            if "/api/poster/" in url:
                return redirect(request.base_url.split("/api")[0]+url)
            chunkedDownload(url, os.path.join(BANNER_FOLDER, f"tt{id}.png"))
        return send_from_directory(BANNER_FOLDER, f"tt{id}.png")

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
    if url.startswith("base64:"): url = base64.b64decode(url[7:]).decode("utf-8")
    headers = Firefox().headers
    try:
        if request.args.get("headers"): headers.update(json.loads(base64.b64decode(request.args.get("headers")).decode('utf-8')))
    except:
        pass
    
    usePHPProxy = False
    if request.args.get("usePHPProxy") == "true":
        usePHPProxy = True

    r = NET().GET(url, headers=headers, stream=True, usePHPProxy=usePHPProxy)
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
        resp["title"] = movie['title']
        resp["plot"] = movie['plot'][0]
        resp["poster"] = movie["full-size cover url"]
        resp["year"] = movie['year']
        resp["genres"] = ", ".join(movie['genres'][0:3])
        resp["episodeCount"] = "0"

        # Get info that might / might not be in imdb's database
        try: resp["airDate"] = movie['original air date']
        except: resp["airDate"] = "N/A"
        try: resp["rating"] = round(float(movie['rating']), 1)
        except: resp["rating"] = "N/A"
        try: resp["budget"] = movie["box office"]['Budget']
        except: resp["budget"] = "N/A"

        # Create line with informations about movie, \u00A0 is unicode for space in JS
        resp["info"] = f"{resp['rating']}/10\u00A0\u00A0{resp['year']}\u00A0\u00A0{resp['genres']}\u00A0\u00A0"
        
        # Add data based on if its movie / tv show
        if "number of seasons" in movie:
            resp["kind"] = "show"
            resp["NOS"] = movie["number of seasons"]
            resp["info"] += f"{resp['NOS']} Seasons"
        else: 
            resp["kind"] = "movie"
            if "duration" in movie:
                resp["info"] += movie["duration"]
            else:
                resp["info"] += "0h 0m"

        cacheItem(f"Item-{id}.json", "ItemInfoCache", json.dumps(resp))
        rp = resp
    else: rp = json.loads(cached)
    rp["inFavorites"] = requests.get(request.base_url.split("/api")[0] + "/api/isInFavorites/" + id, headers=LAH(request)).json()['status'] == 'ok'
    rp["inPlaylist"] = requests.get(request.base_url.split("/api")[0] + "/api/isInPlaylist/" + id, headers=LAH(request)).json()['status'] == 'ok'

    return jsonify(rp)
