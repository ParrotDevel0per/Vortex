from cryptography.fernet import Fernet
from utils.settings import getSetting
import base64
  
key = getSetting("fernetKey").encode()
f = Fernet(key)
  
def encrypt(text):
    return base64.b64encode(f.encrypt(text.encode())).decode()

def decrypt(token):
    try:
        dec = f.decrypt(base64.b64decode(token.encode())).decode()
        if not dec or "-|-" not in dec: return ""
        return dec
    except:
        return ""