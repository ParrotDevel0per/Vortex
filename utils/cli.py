from utils.settings import getSetting, setSetting
from utils.users import createUser, reinitHome
from utils.paths import CACHE_FOLDER, POSTER_FOLDER
from utils.cliUI import intro
from utils.common import cls
from colorama import Fore
import shutil
import os

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
            if len(cmd) != 3: print("Invalid argument count"); continue
            print(setSetting(cmd[1], cmd[2]))

        elif cmd[0].lower() == "get":
            if len(cmd) != 2: print("Invalid argument count"); continue
            print(getSetting(cmd[1]))

        elif cmd[0].lower() == "log":
            print(open(logFile, 'r').read() if open(logFile, 'r').read() != "" else "Log is empty")

        elif cmd[0].lower() == "clear":
            if len(cmd) != 2: print("Invalid argument count"); continue
            if cmd[1].lower() == "cache":
                shutil.rmtree(CACHE_FOLDER)
                os.makedirs(CACHE_FOLDER)
            elif cmd[1].lower() == "posters":
                shutil.rmtree(POSTER_FOLDER)
                os.makedirs(POSTER_FOLDER)
            else: print("Invalid second argument")

        elif cmd[0].lower() == "user":
            if len(cmd) < 2: print("Invalid argument count"); continue
            if cmd[1].lower() == "create":
                if len(cmd) < 4: print("Invalid argument count"); continue

                r = createUser(
                    username=cmd[2],
                    password=cmd[3],
                    email="" if len(cmd) != 5 else cmd[4],
                    admin=False if len(cmd) != 6 else cmd[5] == 'true',
                )
                print("Username already exists" if "already" in r else "User created")
            else: print("Invalid second argument")

        elif cmd[0].lower() == "fix":
            reinitHome()
            print("Everything should work now")
            


     
        elif cmd[0].lower() == "": continue
        else: print("Invalid command")