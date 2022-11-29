from flask import Blueprint, render_template

admin = Blueprint("admin", __name__)

@admin.route('/')
def index():
    return render_template("admin.html")

@admin.route('/terminal')
def terminal():
    return render_template("terminal.html")
