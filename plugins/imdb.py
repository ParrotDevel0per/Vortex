import imdb as imdb
import requests
from utils.common import sanitize, insertInMiddle
from classes.browser import Firefox
from urllib.parse import quote
import re

ia = imdb.Cinemagoer(accessSystem="web")

def runWhileNotDone(do):
    MAX = 20
    attemps = 0
    while attemps <= MAX:
        attemps += 1

        try:
            resp = eval(do)
            #print("Attempt " + str(attemps))
            if resp: return resp
        except: pass
    return {}

"""
def search(query):
    movies = runWhileNotDone(f"ia.search_movie('{sanitize(query)}')")
    response = {}
    for movie in movies:
        if dict(movie)["kind"] not in ["video movie", "movie", "tv series"]: continue
        if "podcast" in dict(movie)["title"].lower(): continue
        response[movie.getID()] = dict(movie)
        response[movie.getID()]["id"] = f"tt{movie.getID()}"
    return response
"""

def search(query):
    firefox = Firefox()
    resp = requests.get(f"https://v3.sg.media-imdb.com/suggestion/titles/x/{quote(query)}.json?includeVideos=0", headers=firefox.headers)
    response = {}
    for movie in resp.json()['d']:
        if movie["qid"] not in ["movie", "tvSeries"]: continue
        if "i" not in movie: continue
        
        response[movie["id"]] = {
            "title": movie["l"],
            #"year": movie["y"],
            "kind": movie["qid"],
            "id": movie["id"],
            "poster": f"/api/poster/{movie['id']}?do=show"
        }
    return response


def seasons(id):
    series = ia.get_movie(id)
    ia.update(series, "episodes")
    result = {}
    result["title"] = dict(series)["title"]
    result["poster"] = dict(series)["full-size cover url"]
    result["seasons"] = len(sorted(series['episodes']))
    return result

def episodes(id, season):
    series = ia.get_movie(id)
    #ia.update(series, "episodes")
    result = {}
    result["title"] = dict(series)["title"]
    result["poster"] = dict(series)["full-size cover url"]
    episodes = series['episodes'][int(season)]
    for ep in episodes:
        result[ep] = {
            "title": episodes[ep]["title"]
        }
    return result

def allEpisodesCount(id):
    series = ia.get_movie(id)
    ia.update(series, "episodes")
    result = {}
    seasons = series['episodes']
    for season in seasons:
        result[season] = len(series['episodes'][season])
    return result

def createPlaylistFromSeries(id):
    series = ia.get_movie(id)
    ia.update(series, "episodes")
    result = {}
    result["title"] = dict(series)["title"]
    result["id"] = f"tt{id}"
    result["poster"] = dict(series)["full-size cover url"]
    se = {}
    for season in series['episodes']:
        s = {}
        for ep in series['episodes'][season]:
            s[ep] = {
                "title": series['episodes'][season][ep]["title"],
                "group": f"{result['title']} - Season {season}"
            }
        se[season] = s
    result["seasons"] = se
    return result

def top250movies():
    movies = ia.get_top250_movies()
    response = {}
    for movie in movies:
        response[movie.getID()] = dict(movie)
        response[movie.getID()]["id"] = f"tt{movie.getID()}"
    return response

def bottom100movies():
    movies = ia.get_bottom100_movies()
    response = {}
    for movie in movies:
        response[movie.getID()] = dict(movie)
        response[movie.getID()]["id"] = f"tt{movie.getID()}"
    return response

def IMDBtoPoster(id):
    try:
        movie = ia.get_movie(id.replace(".png", ""))
        return dict(movie)["full-size cover url"]
    except: return None

def getMovieInfo(id):
    if id.startswith("tt"): id = id.replace("tt", "")
    data = dict(ia.get_movie(id))
    if "number of seasons" not in data:
        duration = re.findall(
                        r"\"duration\"\:\"(.*?)\"",
                        requests.get(f"https://www.imdb.com/title/tt{id}", headers=Firefox().headers).text,
                        re.MULTILINE
                    )[1][2:]
        data["duration"] = insertInMiddle(duration, " ").lower()
    return data
        
            

def getEpisodeInfo(id, season, episode):
    series = ia.get_movie(id)
    ia.update(series, "episodes")
    return dict(series), dict(series['episodes'][int(season)][int(episode)])

def getMoviesByGenres(genres):
    results = ia.get_top50_movies_by_genres(genres)
    resp = {}
    for item in results:
        resp[item.movieID] = {
            "title": item["title"],
            #"plot": item["plot"], NOTE: removed due to cinemagoer update, in no longer grabs plot 
            "full-size cover url": item["full-size cover url"],
            "id": f"tt{item.movieID}"
        }
    return resp