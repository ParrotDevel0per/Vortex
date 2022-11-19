import subprocess
import os
from utils.settings import getSetting, setSetting
from utils.common import get_simple_keys
import sys

class OpenVPN:
    def __init__(self):
        locations = {
            "win32": [
                "C:\\Program Files\\OpenVPN\\bin\\openvpn.exe",
                "C:\\Program Files (x86)\\OpenVPN\\bin\\openvpn.exe"
            ],
            "darwin": [
                "/Applications/OpenVPN Connect/OpenVPN Connect.app/contents/MacOS/OpenVPN Connect"
            ]
        }
        self.cdir = os.getcwd()

        if sys.platform in ["linux", "linux2"]:
            self.openvpn = "openvpn"

        elif sys.platform in get_simple_keys(locations):
            for path in locations[sys.platform]:
                if os.path.exists(path):
                    self.openvpn = path
                    break

        else:
            setSetting("OpenVPNEnabled", "False")
            raise Exception("OS is not supported")

    def connect(self, config=None, auth=None):
        if not os.path.exists(os.path.join(self.cdir, "openvpn")): return
        if not os.path.exists(os.path.join(self.cdir, "openvpn", "configs")): return

        if config == None:
            if getSetting("OpenVPNCFG") and os.path.exists(os.path.join("openvpn", "configs", getSetting("OpenVPNCFG"))):
                config = getSetting("OpenVPNCFG")

        if auth == None:
            if getSetting("OpenVPNAuth") and os.path.exists(os.path.join("openvpn", "auth", getSetting("OpenVPNAuth"))):
                auth = getSetting("OpenVPNAuth")

        if config == None: return
        if not config.endswith(".ovpn"):
            config += ".ovpn"

        if auth and auth.endswith(".txt") == False:
            auth += ".txt"

        config = os.path.join(self.cdir, "openvpn", "configs", config)
        if auth:
            auth = os.path.join(self.cdir, "openvpn", "auth", auth)

        if not os.path.exists(config): return
        command = [self.openvpn, f"--config", config]

        if auth:
            if not os.path.exists(auth): return
            command.append(f"--auth-user-pass {auth}")
        
        subprocess.Popen(" ".join(command), close_fds=True)


