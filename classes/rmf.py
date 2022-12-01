class ResolvedMediaFile:
    def __init__(self, url, headers, refresher={}):
        self.url = url
        self.hlsurl = self.url
        self.headers = headers
        self.refresher = refresher
