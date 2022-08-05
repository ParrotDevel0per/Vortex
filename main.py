from flask import Flask
from api.routes import api
from www.routes import www

ip = "192.168.1.16"
port = 8080

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(www, url_prefix='/')
app.config['JSON_SORT_KEYS'] = False
app.run(host=ip, port=port, debug=True)