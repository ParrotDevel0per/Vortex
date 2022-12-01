class Plugin:
    def __init__(self) -> None:
        pass

    def __getSubclasses(self):
        return Plugin.__subclasses__()

    def getCSS(self):
        css = {}
        for klass in self.__getSubclasses():
            try: css.update(klass.customCSS())
            except: pass
        return css

    def getBlueprints(self):
        blueprints = []
        for klass in self.__getSubclasses():
            blueprints.append(klass.blueprint())
        return blueprints