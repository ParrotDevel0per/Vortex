import inspect
import os
import shutil
import json
import datetime
from utils.common import cls
from utils.settings import getSetting, setSetting, SETTINGSFILE
from utils.users import createUser
from utils.paths import CACHE_FOLDER, POSTER_FOLDER, DB_FOLDER
from prettytable import PrettyTable

class CLI:
    def __init__(self):
        self.commands = []

        for name, func in inspect.getmembers(CLI, predicate=inspect.isfunction):
            if name.startswith("__") or name.startswith("_CLI"): continue

            self.commands.append({
                "name": name,
                "desc": func.__doc__ if func.__doc__ else "No Description",
                "run": func
            })
    

    def __getSubclassesNames(self):
        """
        Get names of subclasses

        Use _getSubclasses() to get class objects
        """
        return [cls.__name__.lower() for cls in CLI.__subclasses__()]

    def __getSubclasses(self):
        """
        Get classes directly
        
        Use _getSubclassesNames() to get only names
        """
        return CLI.__subclasses__()

    def __getSubclassByName(self, name):
        """
        Get only 1 subclass which matches the name

        returns object
        """

        if name.lower() not in self.__getSubclassesNames(): return None

        for klass in self.__getSubclasses():
            if klass.__name__.lower() == name.lower():
                return klass
        return None

    def exec(self, *args):
        """Execute script file"""

        if len(args) < 1: return "Invalid argument count"

        self.__getSubclassByName("CLIScript")(args[0]).run()

    def exit(self, *args) -> str:
        """Exit CLI and run Vortex"""
        
        return "return"

    def help(self, *args) -> PrettyTable:
        """Show help message"""

        table = PrettyTable(field_names=["Command", "Description"])
        for item in self.commands:
            table.add_row([item['name'], item['desc']])
        return table

    def whoami(self, *args) -> str:
        """Shows current user"""

        return "Admin, I guess"


    def clear(self, *args):
        """Clear terminal"""
        
        cls()

    def ff(self, *args):
        """Exit CLI, Exit Vortex"""

        self.clear()
        exit()

    def update(self, *args):
        """Update Vortex"""

        os.system("git fetch")
        os.system("git merge")

    def set(self, *args) -> str:
        """Set X in settings"""
        
        args = list(args)
        if len(args) < 2: return "Invalid argument count"
        return setSetting(args.pop(0), " ".join(args))

    def get(self, *args) -> str:
        """Get X from settings"""

        if len(args) != 1: return "Invalid argument count"
        return getSetting(args[0])

    def export(self, *args) -> str:
        """Creates settings.tpps that can be imported by runing 'exec settings.tpps'"""

        now = datetime.datetime.now()
        file = f"# Auto-exported by Vortex\n# Exported on {now.strftime('%m/%d/%Y, %H:%M:%S')}\n\n"
        loaded = json.loads(open(SETTINGSFILE, 'r').read())
        for k,v in loaded.items():
            file += f"set {k} {v}\n"

        open("settings.tpps", "w", encoding="utf-8").write(file)
        return "Created settings.tpps"

    def remove(self, *args):
        """Remove cache, posters, ..."""

        if len(args) != 1: return "Invalid argument count"
        if args[0] == "cache":
            shutil.rmtree(CACHE_FOLDER)
            os.makedirs(CACHE_FOLDER)
        elif args[0] == "posters":
            shutil.rmtree(POSTER_FOLDER)
            os.makedirs(POSTER_FOLDER)
        else:
            return "Invalid second argument"

    def log(self, *args):
        """Prints out log"""

        return open(os.path.join(DB_FOLDER, "app.log"), 'r').read() if open(os.path.join(DB_FOLDER, "app.log"), 'r').read() != "" else "Log is empty"


    def web(self, *args):
        """Do http requests"""
        print("ffs")
        print(args)
        data = list(args)
        print(data)
        type = data[0]
        url = data[1]
        headers = json.loads(data[2])
        return " ".join()


    def user(self, *args) -> str:
        """Create, Edit, Remove users"""

        if len(args) < 1: return "Invalid argument count"

        if args[0].lower() == "create":
            if len(args) < 3: return "Invalid argument count"
            r = createUser(
                username=args[1],
                password=args[2],
                email="" if len(args) != 4 else args[3],
                admin=False if len(args) != 5 else args[4] == 'true',
            )
            return "Username already exists" if "already" in r else "User created"
        else:
            return "Invalid second argument"
