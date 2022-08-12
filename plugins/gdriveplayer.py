import requests
import re

def resolveGDrivePlayer(url):
    html = requests.get(url).text
    pattern = r"<a href=\"(.*?)\"><li>Mirror Server</li></a>"
    match = re.search(pattern, html)
    if match:
        return "https:" + match.group(1)
    return None