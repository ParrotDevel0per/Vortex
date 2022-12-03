from flask import Blueprint
from classes.plugin import Plugin

# Route will be on /p/ExamplePlugin/
example = Blueprint("ExamplePlugin", __name__) # ID: ExamplePlugin

class Example(Plugin):
    def __init__(self) -> None:
        self.metadata = {
            "name": "Example Plugin",
            "desc": "Example plugin for vortex",
            "author": "Parrot Developers",
            "id": "ExamplePlugin",
            "logo": "logo.png",
            # For adding custom css use:
            #"css": {
            #    "www.index": "/* Example */"
            #}

            # U can make routes that can be only accessed by specific role: admin, public, if no role is set, it can be accessed by anyone who is logged in
            "admin": [
                "ExamplePlugin.test"
            ]
            #"public": [
            #    "ExamplePlugin.test"
            #]
        }
    
    # Check /p/test
    @example.route("/test")
    def test():
        return "N"
    
    # Required
    def blueprint(self) -> Blueprint:
        return example
