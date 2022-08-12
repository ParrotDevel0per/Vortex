import requests
import re
from plugins.vidembed import getCurrentVidembedURL

def resolveGDrivePlayer(url):
    html = requests.get(url).text
    pattern = r"<a href=\"(.*?)\"><li>Mirror Server</li></a>"
    match = re.search(pattern, html)
    if match: return getCurrentVidembedURL() + match.group(1).split("/")[-1]
    return None