import imdb
ia = imdb.Cinemagoer()

def search(query):
    movies = ia.search_movie(query)
    response = {}
    for movie in movies:
        if dict(movie)["kind"] not in ["video movie", "movie", "tv series"]: continue
        if "podcast" in dict(movie)["title"].lower(): continue
        response[movie.getID()] = dict(movie)
        response[movie.getID()]["id"] = f"tt{movie.getID()}"
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
    return dict(ia.get_movie(id))

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
            "plot": item["plot"],
            "full-size cover url": item["full-size cover url"],
            "id": f"tt{item.movieID}"
        }
    return resp