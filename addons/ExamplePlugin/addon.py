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
        }
    
    # Check /p/test
    @example.route("/test")
    def test():
        return "N"
    
    # Required
    def blueprint(self) -> Blueprint:
        return example
