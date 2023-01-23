from flask import Blueprint, render_template
from utils.paths import DB_FOLDER
import os

admin = Blueprint("admin", __name__)
logFile = os.path.join(DB_FOLDER, "app.log")

@admin.route('/')
def index():
    return render_template("admin.html")

@admin.route('/terminal')
def terminal():
    return render_template("terminal.html")

@admin.route('/log')
def log():
    return render_template("log.html", lines=open(logFile, "r").read().split("\n"))

