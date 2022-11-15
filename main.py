from flask import Flask, request, redirect

# App routes
from routes.api.api import api
from routes.api.favorites import favoritesRT
from routes.api.playlist import playlistRT
from routes.auth import auth
from routes.www import www
from routes.m3u import m3u
from routes.admin import admin

# Proxies
from proxies.vidsrc import vidsrc
from proxies.universal import universal

# Rest
from utils.settings import getSetting
from utils.paths import DB_FOLDER
from utils.banner import intro, lenght, textColor
from utils.common import cls, getLocalIP
from users.users import verify, getAdmins
import requests
import threading
import os
import sys
import logging
from classes.cli import CLI
from classes.cliscript import CLIScript

sysArgv = sys.argv[1:]

logFile = os.path.join(DB_FOLDER, "app.log")
if getSetting("keepLogs").lower() == "false":
    open(logFile, "w").write("")
logging.basicConfig(filename=logFile, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = Flask("The Pirate Player")
app.config['JSON_SORT_KEYS'] = False
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(favoritesRT, url_prefix='/api')
app.register_blueprint(playlistRT, url_prefix='/api')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(www, url_prefix='/')
app.register_blueprint(m3u, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(vidsrc, url_prefix='/proxy/vidsrc')
app.register_blueprint(universal, url_prefix='/proxy/universal')




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
        "api.users",
        "api.promoteDemote",
        "api.banUnban",
        "api.deleteUser_",
        "api.changePassword_"
    ]

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
        cmd = input(textColor + "Admin@ThePiratePlayer$ ")
        if " " in cmd: cmd = cmd.split(" ")
        else: cmd = [cmd]

        for item in runner.commands:
            if cmd[0] != item["name"]: continue
            cmd.pop(0)

            try:
                resp = item["run"](runner, *tuple(cmd))
                if resp == "return": return
            except Exception as e: 
                print(e)
            break


if __name__ == "__main__":
    if len(getAdmins()) == 0:
        #           do    user  psw    email       admin
        CLI().user("create admin admin admin@tpp.com true");

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

