import requests
import base64
from classes.proxy import Proxy

request_settings = {
    "timeout": 30,
    "verify": True
}

#phpProxy = "http://localhost:8081"
#phpProxyEnabled = True

class NET:
    def __init__(self) -> None:
        pass
        
    def GET(self, url, headers={}, allow_redirects=True, stream=False):
        if False:
            #if allow_redirects:
            #    headers["X-PHPProxy-AllowRedirects"] = True

            r = requests.get(
                f"https://PunyAcceptableCopyleft.parrotdevelopers.repl.co/get.php?url={base64.b64encode(url.encode()).decode()}",
                headers=headers
            )
            print(r.text)

            return r

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
        if False:
            print(url)
            if allow_redirects:
                headers["X-PHPProxy-AllowRedirects"] = True

            return requests.post(
                f"{phpProxy}/post.php?url={base64.b64encode(url.encode()).decode()}",
                headers=headers,
                timeout=request_settings["timeout"],
                data=data
            )

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
        raise NotImplementedError
        s = requests.Session()
        p = Proxy()
        if p.useproxy: s.proxies.update(p.json())
        return s