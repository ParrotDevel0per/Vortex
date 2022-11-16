import json
import os
import json
from utils.paths import DB_FOLDER

class UserData:
    def __init__(self):
        self.userdata = os.path.join(DB_FOLDER, "userdata.json")
        if not os.path.exists(self.userdata): open(self.userdata, 'w').write("{}")

    def checkIfExists(self):
        if not os.path.exists(self.userdata): open(self.userdata, 'w').write("{}")

    def write(self, k, v):
        self.checkIfExists()
        loaded = json.loads(open(self.userdata, 'r').read())
        loaded[k] = v
        open(self.userdata, 'w').write(json.dumps(loaded))

    def remove(self, k):
        self.checkIfExists()
        loaded = json.loads(open(self.userdata, 'r').read())
        if k in loaded:
            del loaded[k]
            open(self.userdata, 'w').write(json.dumps(loaded))

    def read(self, k, ret=""):
        self.checkIfExists()
        loaded = {}

        attempts = 0
        while attempts <= 10:
            try:
                loaded = json.loads(open(self.userdata, 'r').read())
                break
            except:
                attempts+=1


        if k in loaded:
            return loaded[k]
        return ret

    def DB(self): return json.loads(open(self.userdata, 'r').read())