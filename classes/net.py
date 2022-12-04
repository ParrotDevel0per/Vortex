import requests
import base64
import json
from classes.proxy import Proxy
from utils.settings import getSetting
from utils.users import LAH

request_settings = {
    "timeout": 30,
    "verify": True
}

class NET:
    def __init__(self) -> None:
        self.phpProxyURL = getSetting("phpProxyURL")
        
    def GET(self, url, headers={}, allow_redirects=True, stream=False, usePHPProxy=getSetting("phpProxyEnabled").lower() == "true"):
        if usePHPProxy:
            if allow_redirects:
                headers["X-PHPProxy-AllowRedirects"] = "true"

            return requests.get(
                f"{self.phpProxyURL}/get.php?url={base64.b64encode(url.encode()).decode()}&headers={base64.b64encode(json.dumps(headers).encode()).decode()}",
                allow_redirects=False
            )

        return requests.get(
            url,
            headers=headers,
            allow_redirects=allow_redirects,
            verify=request_settings["verify"],
            timeout=request_settings["timeout"],
            proxies=Proxy().json(),
            stream=stream
        )

    def POST(self, url, headers={}, data=None, allow_redirects=True, usePHPProxy=getSetting("phpProxyEnabled").lower() == "true"):
        if usePHPProxy:
            settingHeaders = {}
            if allow_redirects:
                settingHeaders["X-PHPProxy-AllowRedirects"] = "true"
            
            return requests.post(
                f"{self.phpProxyURL}/post.php?url={base64.b64encode(url.encode()).decode()}&headers={base64.b64encode(json.dumps(headers).encode()).decode()}&data={base64.b64encode(json.dumps(data).encode()).decode()}",
                headers=settingHeaders,
                allow_redirects=False
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

    def get(self, url, headers={}, allow_redirects=True, stream=False):
        return self.GET(url, headers=headers, allow_redirects=allow_redirects, stream=stream)

    def post(self, url, headers={}, data=None, allow_redirects=True):
        return self.POST(url, headers=headers, data=data, allow_redirects=allow_redirects)

    def Session(self):
        return NET()

    def localGET(self, request, path):
        return requests.get(request.url_root[:-1] + path, headers=LAH(request))

    def localPOST(self, request, path, data):
        return requests.post(request.url_root[:-1] + path, headers=LAH(request), data=data)
