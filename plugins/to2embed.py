import re
import requests
from utils.common import girc
from utils.fakeBrowser import baseHeaders

def grab(url):
    headers = baseHeaders
    resp = requests.get(url, headers=headers)
    dataID = re.findall(r'data-id="(.*?)">Server Streamlare</a>', resp.text, re.MULTILINE)[0]
    token = girc(
       requests.get(url).text,
        url,
        'aHR0cHM6Ly93d3cuMmVtYmVkLnRvOjQ0Mw..' # Decoded: https://2embed.to:443
    )

    headers["Referer"] = url
    return requests.get(f"https://www.2embed.to/ajax/embed/play?id={dataID}&_token={token}", headers=headers).json()["link"]


