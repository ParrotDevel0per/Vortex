from flask import Blueprint
from classes.plugin import Plugin

blueprint = Blueprint("Example Plugin", __name__)

class Example(Plugin):
    def __init__(self) -> None:
        super().__init__()
    
    # Check /p/test
    @blueprint.route("/test")
    def test():
        return "N"

    """
    # Add custom css to any part of Vortex
    def customCSS():
        return {
            "www.index": "/* Example */"
        }
    """
    
    # Required
    def blueprint() -> Blueprint:
        return blueprint
