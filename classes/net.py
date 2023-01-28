import requests
import base64
import json
from classes.proxy import Proxy
from utils.settings import getSetting
from utils.users import LAH
from requests.adapters import HTTPAdapter, Retry

request_settings = {
    "timeout": 120,
    "verify": True,
    "max-retries": 10
}

class NET:
    def __init__(self) -> None:
        self.phpProxyURL = getSetting("phpProxyURL")
        
    def GET(self, url, headers={}, cookies={}, allow_redirects=True, stream=False, usePHPProxy=False, useProxy=False):
        if usePHPProxy:
            if allow_redirects:
                headers["X-PHPProxy-AllowRedirects"] = "true"

            return requests.get(
                f"{self.phpProxyURL}/get.php?url={base64.b64encode(url.encode()).decode()}&headers={base64.b64encode(json.dumps(headers).encode()).decode()}",
                allow_redirects=False
            )

        proxies = Proxy().json()
        if useProxy == False:
            proxies = {}

        s = requests.Session()
        retries = Retry(total=request_settings["max-retries"], backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
        s.mount('http://', HTTPAdapter(max_retries=retries))
        s.mount('https://', HTTPAdapter(max_retries=retries))

        return s.get(
            url,
            headers=headers,
            allow_redirects=allow_redirects,
            verify=request_settings["verify"],
            timeout=request_settings["timeout"],
            cookies=cookies,
            proxies=proxies,
            stream=stream
        )

    def POST(self, url, headers={}, cookies={}, data=None, allow_redirects=True, usePHPProxy=False, useProxy=False):
        if usePHPProxy:
            settingHeaders = {}
            if allow_redirects:
                settingHeaders["X-PHPProxy-AllowRedirects"] = "true"
            
            return requests.post(
                f"{self.phpProxyURL}/post.php?url={base64.b64encode(url.encode()).decode()}&headers={base64.b64encode(json.dumps(headers).encode()).decode()}&data={base64.b64encode(json.dumps(data).encode()).decode()}",
                headers=settingHeaders,
                allow_redirects=False
            )

        proxies = Proxy().json()
        if useProxy == False:
            proxies = {}

        s = requests.Session()
        retries = Retry(total=request_settings["max-retries"], backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
        s.mount('http://', HTTPAdapter(max_retries=retries))
        s.mount('https://', HTTPAdapter(max_retries=retries))


        return s.post(
            url,
            headers=headers,
            data=data,
            allow_redirects=allow_redirects,
            verify=request_settings["verify"],
            timeout=request_settings["timeout"],
            proxies=proxies,
            cookies=cookies,
        )

    def get(self, url, headers={}, allow_redirects=True, stream=False, useProxy=False, usePHPProxy=False):
        return self.GET(url, headers=headers, allow_redirects=allow_redirects, stream=stream, useProxy=useProxy, usePHPProxy=usePHPProxy)

    def post(self, url, headers={}, data=None, allow_redirects=True, useProxy=False, usePHPProxy=False):
        return self.POST(url, headers=headers, data=data, allow_redirects=allow_redirects, useProxy=useProxy, usePHPProxy=usePHPProxy)

    def Session(self):
        return NET()

    def localGET(self, request, path):
        return requests.get(request.url_root[:-1] + path, headers=LAH(request))

    def localPOST(self, request, path, data):
        return requests.post(request.url_root[:-1] + path, headers=LAH(request), data=data)
