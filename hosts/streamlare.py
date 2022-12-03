from classes.browser import Firefox
import json
from urllib.parse import urlparse
from classes.net import NET

class StreamLare:
    def __init__(self):
        self.firefox = Firefox()

    def get_redirect_url(self, url, headers={}, form_data=None):
        return NET().GET(url, headers=headers, allow_redirects=False).headers.get('location') or url

    def grab(self, url):
        parsed = urlparse(url)
        host = parsed.netloc
        media_id = parsed.path.replace("/e/", "").replace("/d/", "")

        api_durl = 'https://{0}/api/video/download/get'.format(host)
        api_surl = 'https://{0}/api/video/stream/get'.format(host)
        headers = {'User-Agent': self.firefox.ua,
                'Referer': url,
                'X-Requested-With': 'XMLHttpRequest'}
        data = {'id': media_id}
        html = NET().POST(api_surl, headers=headers, data=data).json()
        result = html.get('result', {})
        source = result.get('file') \
            or result.get('Original', {}).get('file') \
            or result.get(list(result.keys())[0], {}).get('file')
        if not source:
            html = NET().POST(api_durl, headers=headers, data=data).text
            source = json.loads(html).get('result', {}).get('Original', {}).get('url')
        
        if source:
            headers.pop('X-Requested-With')
            if '?token=' in source:
                source = self.get_redirect_url(source, headers=headers)
            return source, headers
