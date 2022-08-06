from flask import Flask
from api.routes import api
from www.routes import www
from proxies.vidsrc import vidsrc
from proxies.gomo import gomo
from settings import getSetting
import os

if bool(getSetting("checkForUpdates")):
    os.system("git fetch")
    os.system("git merge")

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(www, url_prefix='/')
app.register_blueprint(vidsrc, url_prefix='/proxy/vidsrc')
app.register_blueprint(gomo, url_prefix='/proxy/gomo')
app.config['JSON_SORT_KEYS'] = False
app.run(host=str(getSetting("ip")), port=int(getSetting("port")), debug=bool(getSetting("debug")))