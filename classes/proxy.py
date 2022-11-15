import requests
from classes.browser import Firefox

class Proxy:
    def __init__(self, proxy=None, protocol=None):
        self.protocol = protocol if protocol else "socks4"
        self.proxy = proxy if proxy else "178.48.68.61:4145"
        self.useproxy = False

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
        