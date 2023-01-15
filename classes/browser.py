class Firefox:
    def __init__(self) -> None:
        self.ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0"
        self.version = self.ua.split("Firefox/")[1]
        self.headers = {
            "User-Agent": self.ua,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-site",
            "Sec-GPC": "1",
            "TE": "trailers"
        }
        self.headersCopy = self.headers.copy()

    def addHeader(self, k, v):
        """
        args:
            k (str): Name of header
            v (str): Value of header
        
        Adds header to firefox headers
        """

        self.headers[k] = v

    def addHeaders(self, d):
        """
        args:
            d (dict): Dict of headers
        
        Add dict to firefox headers
        """

        self.headers.update(d)

    def removeHeader(self, k):
        """
        args:
            k (str): Name of header to remove
        """

        if k in self.headers:
            del self.headers[k]

    def removeHeaders(self, l):
        """
        args:
            l (list): List of headers to remove
        """
        for k in l:
            self.removeHeader(k)

    def reInitHeaders(self):
        """
        Revert any changes to headers and use original ones
        """

        self.headers = self.headersCopy