from flask import Flask
from routes.api import api
from routes.www import www
from routes.m3u import m3u
from proxies.vidsrc import vidsrc
from proxies.gomo import gomo
from proxies.vidembed import vidembed
#from proxies.r2embed import r2embed
from proxies.kukajto import kukajto
from utils.settings import getSetting, setSetting
from utils.paths import DB_FOLDER
from colorama import init, Fore
import requests
import threading
import os
import sys
import logging
import socket
init()

sysArgv = sys.argv[1:]

logFile = os.path.join(DB_FOLDER, "app.log")
logging.basicConfig(filename=logFile, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = Flask("The Pirate Player")
app.config['JSON_SORT_KEYS'] = False
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(www, url_prefix='/')
app.register_blueprint(m3u, url_prefix='/')
app.register_blueprint(vidsrc, url_prefix='/proxy/vidsrc')
app.register_blueprint(gomo, url_prefix='/proxy/gomo')
app.register_blueprint(vidembed, url_prefix='/proxy/vidembed')
#app.register_blueprint(r2embed, url_prefix='/proxy/2embed')
app.register_blueprint(kukajto, url_prefix='/proxy/kukajto')


def getLocalIP():
    ip = getSetting('ip')
    hostname = socket.gethostname()
    if ip == "0.0.0.0":return socket.gethostbyname(hostname)
    return ip

def cls():
    if os.name == "nt": os.system("cls")
    else: os.system("clear")

banner = """
 __ __|  |                 _ \  _)              |               _ \   |                           
    |    __ \    _ \      |   |  |   __|  _` |  __|   _ \      |   |  |   _` |  |   |   _ \   __| 
    |    | | |   __/      ___/   |  |    (   |  |     __/      ___/   |  (   |  |   |   __/  |    
   _|   _| |_| \___|     _|     _| _|   \__,_| \__| \___|     _|     _| \__,_| \__, | \___| _|    
                                                                               ____/              
"""

lenght = len(banner.split("\n")[1])

def intro():
    print(
        Fore.GREEN,
        banner.center(os.get_terminal_size().columns)
    )
    print("=" * lenght)


@app.before_first_request
def before_first_request_func():
    cls()
    intro()
    print(
        Fore.GREEN,
        f"Running on: http://{getSetting('ip')}:{getSetting('port')}".center(lenght)
    )

help = [
    "help - Shows This Message",
    "exit - Exit CLI and run TPP",
    "whoami - Shows current user",
    "ff - Exit CLI and don't run TPP",
    "update - Checks for updates",
    "set <key> <value> - Set setting to specific value",
    "get <key> - Gets value of key",
    "log - Show log of TPP",
]

def cli():
    cls()
    intro()
    print(
        Fore.GREEN,
        f"Running is paused, write \"exit\" to exit CLI, or write \"ff\" to exit The Pirate Player".center(lenght)
    )
    print("\n" * 2)
    while True:
        cmd = input(Fore.GREEN + "Admin@ThePiratePlayer$ ")
        if " " in cmd: cmd = cmd.split(" ")
        else: cmd = [cmd]

        if cmd[0].lower() == "exit": return
        elif cmd[0].lower() == "help": print("\n".join(help))
        elif cmd[0].lower() == "whoami": print("Admin, I guess")
        elif cmd[0].lower() == "ff": cls(); exit()
        elif cmd[0].lower() == "update":
            os.system("git fetch")
            os.system("git merge")
        elif cmd[0].lower() == "set":
            if len(cmd) != 3: print("Invalid argument count")
            else: print(setSetting(cmd[1], cmd[2]))
        elif cmd[0].lower() == "get":
            if len(cmd) != 2: print("Invalid argument count")
            else: print(getSetting(cmd[1]))
        elif cmd[0].lower() == "log": print(open(logFile, 'r').read() if open(logFile, 'r').read() != "" else "Log is empty")
        elif cmd[0].lower() == "": continue
        else: print("Invalid command")



def sendFirstRequest():
    running = False
    while not running:
        try: requests.get(f"http://{getLocalIP()}:{getSetting('port')}", timeout=1); running = True
        except: pass


if __name__ == "__main__":
    cls()
    intro()
    if "--cli" in sysArgv: cli()
    elif "--nocli" in sysArgv: pass
    else:
        do = input("Do you want to enter admin CLI? [Y/n] ")
        if do.lower() == "y": cli()
        else: pass

    if "--sveltedebug" in sysArgv: os.system("npm run build")

    threading.Thread(target=sendFirstRequest).start()
    app.run(host=str(getSetting("ip")), port=int(getSetting("port")), debug="--debug" in sysArgv)

