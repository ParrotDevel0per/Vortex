from utils.paths import USERDATA
import os
from datetime import datetime

FILENAME = "app.log"
LOG_FILE = os.path.join(USERDATA, FILENAME)

def init():
    open(LOG_FILE, "w").write("")

def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        f.close()
