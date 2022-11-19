import requests
from classes.proxy import Proxy

request_settings = {
    "timeout": 30,
    "verify": True
}

class NET:
    def __init__(self) -> None:
        pass
        
    def GET(self, url, headers={}, allow_redirects=True, stream=False):
        return requests.get(
            url,
            headers=headers,
            allow_redirects=allow_redirects,
            verify=request_settings["verify"],
            timeout=request_settings["timeout"],
            proxies=Proxy().json(),
            stream=stream
        )

    def POST(self, url, headers={}, data=None, allow_redirects=True):
        return requests.post(
            url,
            headers=headers,
            data=data,
            allow_redirects=allow_redirects,
            verify=request_settings["verify"],
            timeout=request_settings["timeout"],
            proxies=Proxy().json()
        )

    def Session(self):
        s = requests.Session()
        p = Proxy()
        if p.useproxy: s.proxies.update(p.json())
        return s