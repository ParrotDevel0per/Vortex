import imdb
ia = imdb.Cinemagoer()

def search(query):
    movies = ia.search_movie(query)
    response = {}
    for movie in movies:
        if dict(movie)["kind"] not in ["video movie", "movie"]: continue
        if "podcast" in dict(movie)["title"].lower(): continue
        response[movie.getID()] = dict(movie)
        response[movie.getID()]["id"] = f"tt{movie.getID()}"
    return response

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
    return dict(ia.get_movie(id))