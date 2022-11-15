from classes.cli import CLI

class CLIScript(CLI):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.tokens = []
        self.__tokenize()
    
    def __tokenize(self):
        data = open(self.path, 'r').read()
        for cmd in data.splitlines():
            if cmd.startswith("#"): continue
            if " " in cmd: cmd = cmd.split(" ")
            else: cmd = [cmd]

            for item in self.commands:
                if cmd[0] != item["name"]: continue
                cmd.pop(0)

                try:
                    self.tokens.append((item["run"], tuple(cmd), ))
                except Exception as e: 
                    print(e)
                break

    def run(self):
        for fn, args in self.tokens:
            resp = fn(self, *args)
            if resp == "return": return