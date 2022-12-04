from flask import Flask, request, redirect, render_template

# App routes
from routes.api.api import api
from routes.api.favorites import favoritesRT
from routes.api.playlist import playlistRT
from routes.auth import auth
from routes.www import www
from routes.m3u import m3u
from routes.admin import admin

# Rest
from utils.settings import getSetting
from utils.paths import DB_FOLDER, ADDONS_FOLDER
from utils.banner import intro, lenght, textColor
from utils.common import cls, getLocalIP
from utils.users import verify, getAdmins
import requests
import threading
import os
import sys
import logging
import sys
import time
from classes.cli import CLI
from classes.cliscript import CLIScript
from classes.openvpn import OpenVPN
from classes.plugin import Plugin

for folder in os.listdir(os.path.join(os.path.dirname(__file__), "addons")):
    if folder.startswith("__"): continue
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "addons", folder))
    data = open(os.path.join(os.path.dirname(__file__), "addons", folder, "addon.py"), "r").read()
    exec(data)


for folder in os.listdir(ADDONS_FOLDER):
    if folder.startswith("__"): continue
    sys.path.insert(0, os.path.join(ADDONS_FOLDER, folder))
    data = open(os.path.join(ADDONS_FOLDER, folder, "addon.py"), "r").read()
    exec(data)


sysArgv = sys.argv[1:]

logFile = os.path.join(DB_FOLDER, "app.log")
if getSetting("keepLogs").lower() == "false":
    open(logFile, "w").write("")
if getSetting("logger").lower() == "true":
    logging.basicConfig(filename=logFile, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = Flask("Vortex")
app.config['JSON_SORT_KEYS'] = False
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(favoritesRT, url_prefix='/api')
app.register_blueprint(playlistRT, url_prefix='/api')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(www, url_prefix='/')
app.register_blueprint(m3u, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')

plugin = Plugin()

css = plugin.css

for bp in plugin.blueprints:
    app.register_blueprint(bp, url_prefix=f'/p/{bp.name}')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.after_request
def overrideResponse(response):
    endpoint = request.endpoint
    if endpoint in css and css[endpoint] and endpoint.startswith(("api.", ) == False):
        response.data =  f"<!--CSS Injected by plugin-->\n<style>{css[endpoint]}</style>\n\n{response.data.decode()}"
    return response


@app.before_request
def verifyRequest():
    endpoint = request.endpoint
    public = [ # You dont need to be logged in for these endpoints
        "api.poster",
        "auth.login_",
        "static"
    ]
    admin = [ # These endpoints require admin rights
        "auth.create_",
        "admin.index",
        "admin.terminal",
        "api.terminal",
        "api.users",
        "api.promoteDemote",
        "api.banUnban",
        "api.deleteUser_",
        "api.changePassword_",
        "api.requestsIP",
        "www.p"
    ]

    public.extend(plugin.access["public"])
    admin.extend(plugin.access["admin"])

    if endpoint in admin:
        #print(endpoint)
        if verify(request, verifyAdmin=True) == False:
            return "Forbidden", 403
    
    if endpoint not in public:
        #print(endpoint)
        if verify(request) == False:
            return redirect("/login")

@app.before_first_request
def before_first_request_func():
    cls()
    intro()
    ip = getSetting('ip')
    if ip == "0.0.0.0": ip = "localhost"
    print(textColor, f"Running on: http://{ip}:{getSetting('port')}".center(lenght))

def sendFirstRequest():
    running = False
    while not running:
        try: requests.get(f"http://{getLocalIP()}:{getSetting('port')}", timeout=1); running = True
        except: pass

def cli():
    cls()
    intro()

    runner = CLI()

    while True:
        cmd = input(textColor + "Admin@Vortex$ ")
        if " " in cmd: cmd = cmd.split(" ")
        else: cmd = [cmd]

        for item in runner.commands:
            if cmd[0] != item["name"]: continue
            cmd.pop(0)

            try:
                resp = item["run"](runner, *tuple(cmd))
                if resp == "return": return
                else: print(resp)
            except Exception as e: 
                print(e)
            break


if __name__ == "__main__":
    if getSetting("OpenVPNEnabled").lower() == "true":
        try: OpenVPN().connect()
        except Exception as e:
            print(e)
            time.sleep(3)

    if len(getAdmins()) == 0:
        CLI().user("create", "admin", "admin", "admin@tpp.com", "true");

    if os.path.exists("autoexec.tpps"):
        CLIScript("autoexec.tpps").run()


    cls()
    intro()
    if "--cli" in sysArgv:
        cli()
    elif "--nocli" in sysArgv:
        pass
    else:
        do = input("Do you want to enter admin CLI? [Y/n] ")
        if do.lower() == "y": cli()
        else: pass

    if "--sveltedebug" in sysArgv:
        os.system("npm run dev")

    threading.Thread(target=sendFirstRequest).start()
    app.run(host=str(getSetting("ip")), port=int(getSetting("port")), debug="--debug" in sysArgv)

