from utils.common import randStr
from utils.userdata import UserData
from utils.crypto import encrypt, decrypt
import hashlib
import time

UD = UserData()

def defaultHome():
    return [
		{
			"title": "Action",
			"url": "/api/getMoviesByGenres?genres=Action",
		},
		{
			"title": "War",
			"url": "/api/getMoviesByGenres?genres=War",
		},
        {
			"title": "History",
			"url": "/api/getMoviesByGenres?genres=History",
		},
        {
			"title": "Western",
			"url": "/api/getMoviesByGenres?genres=Western",
		},
    ]

def getIP(req):
    ip = str(req.remote_addr)
    if ip: return ip
    return "IDK"

def login(username, password):
    uid = usernameToUID(username)
    data = UD.read(uid)
    if not data: return False
    if hashlib.sha512(password.encode()).hexdigest() != data["password"]: return False
    return encrypt(f"{username}-|-{password}-|-{uid}-|-{int(str(time.time()).split('.')[0])}")

def createUser(username, password, email="", admin=False, banned=False):
    UID = randStr(64)
    if UD.read(usernameToUID(username), ret="") != "": return "Username already exists"

    user = {
        "UID": UID,
        "username": username,
        "password": hashlib.sha512(password.encode()).hexdigest(),
        "isAdmin": admin,
        "favorites": {},
        "playlist": {},
        "history": {},
        "home": defaultHome(),
        "email": email,
        "createdOn": int(str(time.time()).split(".")[0]),
        "isBanned": banned,
        "ip": "0.0.0.0",
    }

    UD.write(UID, user)
    return login(username, password)

def usernameToUID(username):
    db = UD.DB()
    for key in db:
        if db[key]["username"] == username:
            return db[key]["UID"]
    return ""

def uids():
    us = []
    db = UD.DB()
    for key in db:us.append(key)
    return us
    

def reinitHome():
    for u in uids():
        changeValue(
            u,
            "home",
            defaultHome()
        )

def deleteUser(UID):
    UD.remove(UID)

def LAH(request):
    return {"Authorization": f"Parrot {reqToToken(request)}"}

def reqToToken(req):
    if "token" in req.cookies: return req.cookies.get("token")
    elif "token" in req.args: return req.args.get("token")
    elif "Authorization" in req.headers: return req.headers.get("Authorization").split("Parrot ")[1]
    elif "username" in req.args: return login(req.args.get("username"), req.args.get("password"))
    elif "username" in req.headers: return login(req.headers.get("username"), req.headers.get("password"))
    return ""

def verify(req, verifyAdmin=False):
    token = reqToToken(req)
    if not token: return False

    decrypted = decrypt(token)
    if not decrypted: return False
    # Structure
    #   Username-|-Password-|-UID-|-createdOn
    username, password, uid, createdOn = decrypted.split("-|-")
    if int(time.time()) > int(createdOn) + (30 * 60 * 60 * 24): return False
    data = UD.read(uid)
    if not data: return False
    if hashlib.sha512(password.encode()).hexdigest() != data["password"]: return False
    
    if verifyAdmin:
        if data['isAdmin'] != True:
            return False

    ip = getIP(req)

    try: changeValue(uid, "ip", ip)
    except: pass

    return True

def tokenToUID(token):
    decrypted = decrypt(token)
    if not decrypted: return False
    uid = decrypted.split("-|-")[2]
    return uid

def reqToUID(req):
    return tokenToUID(reqToToken(req))

def userdata(UID):
    return UD.read(UID)

def readValue(UID, k):
    return UD.read(UID)[k]

def changeValue(UID, k, v):
    if v == None: return
    l = UD.read(UID)
    l[k] = v
    UD.write(UID, l)

def changeValues(UID, d):
    if d == None: return
    l = UD.read(UID)
    l.update(d)
    UD.write(UID, l)

def deleteValue(UID, k):
    l = UD.read(UID)
    del l[k]
    UD.write(UID, l)