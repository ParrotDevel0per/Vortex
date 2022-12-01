from colorama import init, Fore
import os
init()

banner = """
\ \     /               |                
 \ \   /    _ \    __|  __|   _ \ \ \  / 
  \ \ /    (   |  |     |     __/  `  <  
   \_/    \___/  _|    \__| \___|  _/\_\ 
   """

lenght = len(banner.split("\n")[2])
textColor = Fore.GREEN

def intro():
    size = 100
    try: size = os.get_terminal_size().columns
    except: pass
    print(
        textColor,
        banner.center(size)
    )
    print("=" * lenght)