import requests
from plugins.imdb import getMovieInfo
from utils.fakeBrowser import UA


def translateItemToCzech(id, isMovie):
    url = "https://www.csfd.cz/api/search/autocomplete/?q=" + getMovieInfo(id)["title"]
    headers = {
        "User-Agent": UA,
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

