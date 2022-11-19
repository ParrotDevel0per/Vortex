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

    def json(self, test_ = False):
        if test_ == False:
            if self.useproxy == False:
                return {}

        return {
            'http': f"{self.protocol}://{self.proxy}",
            'https': f"{self.protocol}://{self.proxy}"
        }

    def test(self):
        try:
            resp = requests.get(
                "https://fast.com/",
                headers=Firefox().headers,
                proxies=self.json(test_=True),
                timeout=30,
                verify=False
            )
        except Exception as e: 
            print("Proxy didnt work, reason:\n", e, sep="")
            return False

        if resp.status_code in range(200, 400):
            return True
        return False
        