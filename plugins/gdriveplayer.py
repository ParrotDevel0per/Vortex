import requests
import re
from plugins.vidembed import getCurrentVidembedURL
from utils.fakeBrowser import baseHeaders

def resolveGDrivePlayer(url):
    html = requests.get(url, headers=baseHeaders).text
    pattern = r"<a href=\"(.*?)\"><li>Mirror Server</li></a>"
    match = re.search(pattern, html)
    if match: return getCurrentVidembedURL() + match.group(1).split("/")[-1]
    return None