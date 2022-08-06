from flask import Flask
from api.routes import api
from www.routes import www
from proxies.vidsrc import vidsrc
from proxies.gomo import gomo
from utils.logger import init, log
from settings import getSetting
init()

ip = str(getSetting("ip"))
port = int(getSetting("port"))

log(f"Starting server on {ip}:{port}")
app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(www, url_prefix='/')
app.register_blueprint(vidsrc, url_prefix='/proxy/vidsrc')
app.register_blueprint(gomo, url_prefix='/proxy/gomo')
app.config['JSON_SORT_KEYS'] = False
app.run(host=ip, port=port, debug=bool(getSetting("debug")))