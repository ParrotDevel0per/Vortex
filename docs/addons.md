# Addons
Vortex has addon (plugin) capabilities. Addons can use any part of vortex, they can also add custom CSS to any endpoint and add own movie / tv shows resolvers. 

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
Example addon with basic capabilities, it is also located in "Preinstalled" directory  

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