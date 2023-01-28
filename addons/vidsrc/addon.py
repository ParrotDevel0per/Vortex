from flask import Blueprint, request, Response
from classes.plugin import Plugin
from classes.browser import Firefox
from classes.net import NET
from bs4 import BeautifulSoup
import re
import time
import base64
from utils.common import randStr
from utils.users import reqToToken
from utils.addonSettings import setAddonSetting, getAddonSetting
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import os
import time
import json

name = "vidsrc"
vidsrcBP = Blueprint(name, __name__)
database = {}
sleepTime = 100 # Interval of updating token
expireAfter = 3 * 60 * 60 # When unused token will expire, must be bigger than sleepTime

def checkIfExpired():
    for key in database:
        if database[key]["expire"] > int(time.time()) + expireAfter:
            del database[key]

def refreshToken(token):
    r = NET().GET(token["refresher"], headers=token["headers"], useProxy=getAddonSetting(name, "useProxy").lower() == "true", usePHPProxy=getAddonSetting(name, "phpProxyEnabled").lower() == "true")
    global database
    database[token["uid"]]["expire"] = int(time.time()) + sleepTime


def retryClick(driver, xpath, max_retries=25):
    for i in range(max_retries):
        try:
            driver.find_element(By.XPATH, xpath).click()
            return
        except:
            time.sleep(1)



@vidsrcBP.route('/playlist.m3u8')
def playlist():
    wmsAuthSign = request.args.get('wmsAuthSign')
    if wmsAuthSign is None: return "Forbidden"
    wmsAuthSign = json.loads(base64.b64decode(wmsAuthSign).decode('utf-8'))
    if wmsAuthSign["uid"] not in database: return "Forbidden"
    if database[wmsAuthSign["uid"]]["expire"] < int(time.time()): refreshToken(wmsAuthSign)
    r = NET().GET(wmsAuthSign['url'], headers=wmsAuthSign["headers"], useProxy=getAddonSetting(name, "useProxy").lower() == "true", usePHPProxy=getAddonSetting(name, "phpProxyEnabled").lower() == "true")
    wmsAuthSign = base64.b64encode(json.dumps(wmsAuthSign).encode('utf-8')).decode('utf-8')
    return Response(r.text.replace("http", f"/p/{name}/ts?url=http").replace(".ts", f".ts&wmsAuthSign={wmsAuthSign}&token={reqToToken(request)}"), mimetype='application/x-mpegURL')

@vidsrcBP.route('/ts')
def ts():
    wmsAuthSign = request.args.get('wmsAuthSign')
    if wmsAuthSign is None: return "Forbidden"
    wmsAuthSign = json.loads(base64.b64decode(wmsAuthSign).decode('utf-8'))
    if wmsAuthSign["uid"] not in database: return "Forbidden"
    if database[wmsAuthSign["uid"]]["expire"] < int(time.time()): refreshToken(wmsAuthSign)
    r = NET().GET(request.args.get("url"), headers=wmsAuthSign["headers"], useProxy=getAddonSetting(name, "useProxy").lower() == "true", usePHPProxy=getAddonSetting(name, "phpProxyEnabled").lower() == "true")
    return Response(r.content, mimetype='video/mp2t')

class VidSrc(Plugin):
    def __init__(self) -> None:
        self.metadata = {
            "name": "VidSrc",
            "desc": "Plugin for grabbing streams from vidsrc.me",
            "author": "Parrot Developers",
            "id": "vidsrc",
            "logo": "logo.png",
            "resolver": {
                "name": "vidsrc",
                "func": self.resolve,
            },
            "settings": ["phpProxyEnabled", "useProxy"],
        }

        if not getAddonSetting(name, "phpProxyEnabled"):
            setAddonSetting(name, "phpProxyEnabled", "false")

        if not getAddonSetting(name, "useProxy"):
            setAddonSetting(name, "useProxy", "false")
    
        if not getAddonSetting(name, "sessionID"):
            setAddonSetting(name, "sessionID", "")

        if not getAddonSetting(name, "sessionExpire"):
            setAddonSetting(name, "sessionExpire", "0")

    def createSession(self):
        options = Options()
        options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.install_addon(os.path.join(os.getcwd(), "extensions", "buster_captcha_solver-2.0.1.xpi"), temporary=True)
        driver.get("https://v2.vidsrc.me/embed/tt7286456")
        iframe = driver.find_element(By.ID, "player_iframe")
        src = iframe.get_attribute("src")
        driver.switch_to.frame(iframe)
        driver.find_element(By.XPATH, '//*[@id="pl_but"]').click()

        # Captcha implementation
        for ciframe in driver.find_elements(By.TAG_NAME, "iframe"):
            try:
                if "recaptcha challenge" in ciframe.get_attribute("title"):
                    driver.switch_to.frame(ciframe)
                    driver.find_element(By.XPATH, "/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[4]").click()
                    time.sleep(3)
                    driver.switch_to.frame(iframe)
                    break
            except:
                pass

        driver.get(src)
        cookies = driver.get_cookies()
        driver.quit()

        for cookie in cookies:
            if cookie['name'] == "PHPSESSID":
                return cookie['value']
        

    def getSession(self):
        if int(getAddonSetting(name, "sessionExpire")) > int(time.time()):
            return getAddonSetting(name, "sessionID")

        session = self.createSession()
        setAddonSetting(name, "sessionID", session)
        setAddonSetting(name, "sessionExpire", str( int(time.time()) + (24 * 60 * 60) ))
        return session
            

    def resolve(self, imdbid, episode=None):
        url = "https://v2.vidsrc.me/embed/{}/".format(imdbid)
        if episode != None: url += "{}/".format(episode)

        cookies = {
            "PHPSESSID": self.getSession()
        }

        firefox = Firefox()
        firefox.addHeader("Referer", "https://vidsrc.me/")
        r = NET().GET(url, headers=firefox.headers, useProxy=getAddonSetting(name, "useProxy").lower() == "true", usePHPProxy=getAddonSetting(name, "phpProxyEnabled").lower() == "true")
        soup = BeautifulSoup(r.text, 'html.parser')
        iframe = soup.find('iframe', id='player_iframe')
        src = iframe['src'].replace('//', 'https://')


        try:
            firefox.addHeader("Referer", src)
            r = NET().GET(src, headers=firefox.headers, cookies=cookies, useProxy=getAddonSetting(name, "useProxy").lower() == "true", usePHPProxy=getAddonSetting(name, "phpProxyEnabled").lower() == "true")
            src = re.search(r'src: \'(.*?)\'', r.text).group(1).replace("//", "https://")
            firefox.addHeader("Referer", src)
            r = NET().GET(src, headers=firefox.headers, allow_redirects=True, useProxy=getAddonSetting(name, "useProxy").lower() == "true", usePHPProxy=getAddonSetting(name, "phpProxyEnabled").lower() == "true")
            hlsurl = re.search(r'video.setAttribute\("src" , "(.*?)"\)', r.text).group(1)
            path = re.findall(r'var path = "(.*?)"', r.text)[1].replace("//", "https://")
        except:
            setAddonSetting(name, "sessionID", "")
            setAddonSetting(name, "sessionExpire", "0")
            return self.resolve(imdbid, episode)
        
        firefox.reInitHeaders()
        firefox.addHeader("Referer", "https://vidsrc.stream/")

        UID = randStr(32)
        NET().GET(path, headers=firefox.headers, useProxy=getAddonSetting(name, "useProxy").lower() == "true", usePHPProxy=getAddonSetting(name, "phpProxyEnabled").lower() == "true").text # ! do not remove this line, otherwise everything gets fucked

        # create wmsAuthSign
        wmsAuthSign = {}
        wmsAuthSign["url"] = hlsurl
        wmsAuthSign["refresher"] = path
        wmsAuthSign["headers"] = firefox.headers
        wmsAuthSign["uid"] = UID
        wmsAuthSign = base64.b64encode(json.dumps(wmsAuthSign).encode('utf-8')).decode('utf-8')
        
        expire = int(time.time()) + sleepTime
        global database
        database.update({
            UID: {
                "expire": expire
            }
        })
        return f"/p/{name}/playlist.m3u8?wmsAuthSign={wmsAuthSign}&token=[[token]]"

    # Required
    def blueprint(self) -> Blueprint:
        return vidsrcBP
