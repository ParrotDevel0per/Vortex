from ..utils.browser import Firefox
from ..utils.resolve import Resolver
from ..utils.unpacker import unpack
import json
from urllib.parse import urlparse
import requests
import six
import urllib.request as urllib_request
import urllib.parse as urllib_parse
import urllib.error as urllib_error

class StreamLare(Resolver):
    def __init__(self):
        self.firefox = Firefox()

    def get_redirect_url(self, url, headers={}, form_data=None):
        class NoRedirection(urllib_request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                return None

        if form_data:
            if isinstance(form_data, dict):
                form_data = urllib_parse.urlencode(form_data)
            request = urllib_request.Request(url, six.b(form_data), headers=headers)
        else:
            request = urllib_request.Request(url, headers=headers)

        opener = urllib_request.build_opener(NoRedirection())
        try:
            response = opener.open(request, timeout=20)
        except urllib_error.HTTPError as e:
            response = e
        return response.headers.get('location') or url

    def grab(self, url, referer):
        parsed = urlparse(url)
        host = parsed.netloc
        media_id = parsed.path.replace("/e/", "").replace("/d/", "")

        api_durl = 'https://{0}/api/video/download/get'.format(host)
        api_surl = 'https://{0}/api/video/stream/get'.format(host)
        headers = {'User-Agent': self.firefox.ua,
                'Referer': url,
                'X-Requested-With': 'XMLHttpRequest'}
        data = {'id': media_id}
        html = requests.post(api_surl, headers=headers, data=data).json()
        result = html.get('result', {})
        source = result.get('file') \
            or result.get('Original', {}).get('file') \
            or result.get(list(result.keys())[0], {}).get('file')
        if not source:
            html = requests.post(api_durl, headers=headers, data=data).text
            source = json.loads(html).get('result', {}).get('Original', {}).get('url')
        if source:
            headers.pop('X-Requested-With')
            if '?token=' in source:
                source = self.get_redirect_url(source, headers=headers)
            return source, headers
