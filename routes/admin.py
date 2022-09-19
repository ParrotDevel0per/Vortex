from flask import Blueprint, request, render_template
from utils.users import verify, LAH, reqToToken
import requests


admin = Blueprint("admin", __name__)

@admin.route('/')
def index():
    if verify(request, verifyAdmin=True) == False: return "Forbidden", 403
    return render_template("admin.html")


