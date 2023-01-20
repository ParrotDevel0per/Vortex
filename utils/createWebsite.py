import requests
import re
import string
import random
from classes.browser import Firefox
from ftplib import FTP

firefox = Firefox()

firefox.addHeaders({
    "Referer": "https://newserv.freewha.com/freewha.cpanel",
    "Origin": "https://newserv.freewha.com"
})


def randStr(length, digits=False, uppercase=False):
    s = ""
    all = string.ascii_lowercase

    if digits:
        all += string.digits

    if uppercase:
        all += string.ascii_uppercase

    for i in range(length):
        s += random.choice(all)
    return s


def register(domain, email, password):
    data = {
        "action": "validate",
        "domainName": domain,
        "email": email,
        "password": password,
        "confirmPassword": password,
        "agree": "1",
    }

    requests.post("https://newserv.freewha.com/cgi-bin/create_ini.cgi",
                  headers=firefox.headers,
                  data=data)
    return {"username": domain, "password": password}


def login(username, password):
    data = {
        "login": username,
        "passwd": password,
        "persistent": "Y",
        "action": "Log+In",
    }

    resp = requests.post("https://newserv.freewha.com/freewha.cpanel",
                         headers=firefox.headers,
                         data=data)
    user_id = re.findall(
        r"<input type=\"hidden\" name=\"user_id\" value=\"(.*?)\">", resp.text,
        re.MULTILINE)[0]
    pid = re.findall(r"<input type=\"hidden\" name=\"pid\" value=\"(.*?)\">",
                     resp.text, re.MULTILINE)[0]

    return user_id, pid, dict(resp.cookies)


def changePHPVersion(user_id, pid, cookies):
    data = f"newphp=73&user_id={user_id}&pid={pid}&persistent=Y&action=Change+PHP+Version"
    requests.post("https://newserv.freewha.com/freewha.cpanel",
                  headers=firefox.headers,
                  data=data,
                  cookies=cookies)


def createWebsite():
    domain = f"{randStr(random.randint(5, 25),)}.orgfree.com"
    email = f"{randStr(random.randint(5, 10))}@gmail.com"
    password = randStr(random.randint(10, 16), digits=True, uppercase=True)

    register(domain, email, password)
    changePHPVersion(*login(domain, password))

    # Upload Site
    ftp = FTP()
    ftp.set_debuglevel(1)
    ftp.connect(domain, 21)
    ftp.login(domain, password)


    ftp.storbinary('STOR get.php', open("./php/get.php", 'rb'))
    ftp.storbinary('STOR post.php', open("./php/post.php", 'rb'))


    ftp.quit()
    return f"http://{domain}"
