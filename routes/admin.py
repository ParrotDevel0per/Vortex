from flask import Blueprint, render_template, request
from utils.paths import DB_FOLDER
from classes.plugin import Plugin
from classes.net import NET
from utils.common import randStr
import os

admin = Blueprint("admin", __name__)
logFile = os.path.join(DB_FOLDER, "app.log")

@admin.route('/')
def index():
    return render_template("admin/index.html")

@admin.route('/terminal')
def terminal():
    return render_template("admin/terminal.html")

@admin.route('/users')
def users():
    return render_template("admin/users.html")

@admin.route('/log')
def log():
    return render_template("admin/log.html", lines=open(logFile, "r").read().split("\n"))


@admin.route("/addons")
def addons(): # Plugins
    return render_template("admin/plugins.html", plugins=Plugin().plugins)

@admin.route("/ps")
def ps(): # Plugin Settings
    id = request.args.get('id')
    if not id:
        return "No ID"
    settings = {}
    for plugin in Plugin().plugins:
        if plugin["id"] == id:
            settings = plugin["settings"]

    settings_ = []
    for setting in settings:
        settings_.append({
            "key": setting,
            "value": NET().localGET(request, f"/api/addonSettings?do=get&id={id}&key={setting}").text,
            "inputID": randStr()
        })
    return render_template("admin/pluginsettings.html", settings=settings_, id=id)