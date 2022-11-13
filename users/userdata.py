import json
import os
import json
from utils.paths import DB_FOLDER

userdata = os.path.join(DB_FOLDER, "userdata.json")
if not os.path.exists(userdata): open(userdata, 'w').write("{}")

class UserData:
    def checkIfExists(self, userdata):
        if not os.path.exists(userdata): open(userdata, 'w').write("{}")

    def write(self, k, v):
        self.checkIfExists(userdata)
        loaded = json.loads(open(userdata, 'r').read())
        loaded[k] = v
        open(userdata, 'w').write(json.dumps(loaded))

    def remove(self, k):
        self.checkIfExists(userdata)
        loaded = json.loads(open(userdata, 'r').read())
        if k in loaded:
            del loaded[k]
            open(userdata, 'w').write(json.dumps(loaded))

    def read(self, k, ret=""):
        self.checkIfExists(userdata)
        try: loaded = json.loads(open(userdata, 'r').read())
        except:
            loaded = {}
            print(open(userdata, 'r').read())
        if k in loaded:
            return loaded[k]
        return ret

    def DB(self): return json.loads(open(userdata, 'r').read())