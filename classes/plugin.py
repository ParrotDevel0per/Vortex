class Plugin:
    def __init__(self) -> None:
        self.css = {}
        self.blueprints = []
        self.resolvers = {}
        self.setData()

    def __getSubclasses(self):
        return Plugin.__subclasses__()

    def setData(self):
        for klass in self.__getSubclasses():
            # Add all blueprints
            self.blueprints.append(klass.blueprint())

            # Add custom css
            try: self.css.update(klass.customCSS())
            except: pass
            
            # Check for resolvers
            try:
                name = klass.resolve.__doc__.split("-")
                self.resolvers[name[0]] = {
                    "run": klass.resolve,
                    "ext": name[1]
                }
            except:
                pass
            
