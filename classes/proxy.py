import requests
from classes.browser import Firefox
from utils.settings import getSetting

class Proxy:
    def __init__(self, proxy=None, protocol=None):
        p = ""
        ps = getSetting("proxy").lower()
        auth = getSetting("proxyAuth")
        if auth: p = f"{auth}@{ps.split(':')[1]}:{ps.split(':')[2]}"

        self.protocol = protocol if protocol else ps.split(":")[0]
        self.proxy = proxy if proxy else p
        self.useproxy = getSetting("useProxy").lower() == 'true'

    def json(self):
        return {
            'http': f"{self.protocol}://{self.proxy}",
            'https': f"{self.protocol}://{self.proxy}"
        }