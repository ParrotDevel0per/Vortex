import  requests
import re
from classes.browser import Firefox
from difflib import get_close_matches

def getBanner(imdbid):
    section = "movies"
    firefox = Firefox()
    title = re.findall(
        r"<title>(.*?)</title>",
        requests.get(f"https://www.imdb.com/title/{imdbid}", headers=firefox.headers).text,
        re.MULTILINE
    )[0].replace(" - IMDb", "")
    if "TV Series" in title:
        section = "tv"

    firefox.addHeader("Referer", "https://fanart.tv/")
    resp = requests.get(f"https://fanart.tv/api/search.php?section={section}&s={title}", headers=firefox.headers)
    titles, links = [], []

    for item in resp.json():
        titles.append(item["title"])
        links.append(item["link"])

    t = title.split(" (")[0] if "("in title else title
    closest = ""

    if t in titles:
        closest = t
    else:    
        try: closest = get_close_matches(t, titles)[0]
        except: closest = titles[0]


    matches = re.findall(
        r"background\" href=\"https:\/\/images\.fanart\.tv\/fanart\/(.*?)\"",
        requests.get(f"{links[titles.index(closest)]}", headers=firefox.headers).text,
        re.MULTILINE
    )

    if len(matches) == 0:
        return f"/api/poster/{imdbid}?do=show"

    return f"https://images.fanart.tv/fanart/{matches[0]}"