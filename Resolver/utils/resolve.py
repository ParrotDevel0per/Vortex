from classes.rmf import ResolvedMediaFile

class Resolver(object):
    """
    Used for communicating with plugins
    """

    def __init__(self):
        pass

    def _getSubclassesNames(self):
        """
        Get names of subclasses

        Use _getSubclasses() to get class objects
        """
        return [cls.__name__.lower() for cls in Resolver.__subclasses__()]

    def _getSubclasses(self):
        """
        Get classes directly
        
        Use _getSubclassesNames() to get only names
        """
        return Resolver.__subclasses__()

    def _getSubclassByName(self, name):
        """
        Get only 1 subclass which matches the name

        returns object
        """

        if name.lower() not in self._getSubclassesNames(): return None

        for klass in self._getSubclasses():
            if klass.__name__.lower() == name.lower():
                return klass
        return None

    def resolve(self, module, imdbid, episode=None):
        """
        Args:
            module (str): Plugin to use
            imdbid (str): imdbid to grab

        Returns:
            rmf (ResolvedMediaFile): use .url or .headers to get data, .test() to test if stream works
        """
        c = self._getSubclassByName(module)()
        c.parent = self
        try:data = c.grab(imdbid, episode)
        except: data = {}
        return ResolvedMediaFile(
            url=data.get("url", ""),
            headers=data.get("headers", {}),
            refresher=data.get("refresher", {}),
        )

