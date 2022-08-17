import requests
from plugins.imdb import getMovieInfo


def translateItemToCzech(id, isMovie):
    url = "https://www.csfd.cz/api/search/autocomplete/?q=" + getMovieInfo(id)["title"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.csfd.cz/",
        "X-Requested-With": "XMLHttpRequest",
        "DNT": "1",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1"
    }

    resp = requests.get(url, headers=headers).json()
    if isMovie: return resp['films'][0]['name']
    return resp['series'][0]['name']

