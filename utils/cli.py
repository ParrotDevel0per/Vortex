import inspect
import os
import shutil
from utils.common import cls
from utils.settings import getSetting, setSetting
from users.users import createUser, reinitHome
from utils.paths import CACHE_FOLDER, POSTER_FOLDER, DB_FOLDER
from utils.banner import intro, textColor

class CLI:
    def __init__(self):
        self.commands = []

        for name, func in inspect.getmembers(CLI, predicate=inspect.isfunction):
            if name.startswith("__"): continue

            self.commands.append({
                "name": name,
                "desc": func.__doc__ if func.__doc__ else "No Description",
                "run": func
            })
    

    def exit(self, *args):
        """Exit CLI and run TPP"""
        
        return "return"

    def help(self, *args):
        """Show help message"""

        for item in self.commands:
            print(f"{item['name']} --- {item['desc']}")

    def whoami(self, *args):
        """Shows current user"""

        print("Admin, I guess")


    def clear(self, *args):
        """Clear terminal"""
        
        cls()

    def ff(self, *args):
        """Exit CLI, Exit TPP"""

        self.clear()
        exit()

    def update(self, *args):
        """Update TPP"""

        os.system("git fetch")
        os.system("git merge")

    def set(self, *args):
        """Set X in settings"""

        if len(args) != 2: print("Invalid argument count"); return
        print(setSetting(args[0], args[1]))

    def get(self, *args):
        """Get X from settings"""

        if len(args) != 1: print("Invalid argument count"); return
        print(getSetting(args[0]))

    def remove(self, *args):
        """Remove cache, posters, ..."""

        if len(args) != 1: print("Invalid argument count"); return
        if args[0] == "cache":
            shutil.rmtree(CACHE_FOLDER)
            os.makedirs(CACHE_FOLDER)
        elif args[0] == "posters":
            shutil.rmtree(POSTER_FOLDER)
            os.makedirs(POSTER_FOLDER)
        else:
            print("Invalid second argument")

    def log(self, *args):
        """Prints out log"""

        print(open(os.path.join(DB_FOLDER, "app.log"), 'r').read() if open(os.path.join(DB_FOLDER, "app.log"), 'r').read() != "" else "Log is empty")

    def user(self, *args):
        """Create, Edit, Remove users"""

        if len(args) < 1: print("Invalid argument count"); return

        if args[0].lower() == "create":
            if len(args) < 3: print("Invalid argument count"); return
            r = createUser(
                username=args[1],
                password=args[2],
                email="" if len(args) != 4 else args[3],
                admin=False if len(args) != 5 else args[4] == 'true',
            )
            print("Username already exists" if "already" in r else "User created")
        else:
            print("Invalid second argument")

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


