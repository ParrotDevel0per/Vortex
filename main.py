from flask import Flask
from api.routes import api
from www.routes import www
from utils.logger import init, log
from settings import getSetting
init()

ip = str(getSetting("ip"))
port = int(getSetting("port"))

log(f"Starting server on {ip}:{port}")
app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(www, url_prefix='/')
app.config['JSON_SORT_KEYS'] = False
app.run(host=ip, port=port, debug=bool(getSetting("debug")))