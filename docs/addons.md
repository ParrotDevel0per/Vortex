# Addons
Vortex has addon (plugin) capabilities. Addons can use any part of vortex, they can also add custom CSS to any endpoint and add own movie / tv shows resolvers. Also addons can change permissions for routes

## Addon directories
Preinstalled:  
```
Vortex/addons
Vortex\addons
```

User installed:  
```
$home/.Vortex/addons
%appdata%\Vortex\addons
```

## Example addon
Example addon with basic capabilities, it is also located in "Preinstalled" directory on every version  

```python
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

```
This addon creates sub-url in /p/ExamplePlugin/test  