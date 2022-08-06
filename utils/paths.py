import os

USERDATA = ""
FOLDERNAME = "ThePiratePlayer"
CACHEFOLDERNAME = "cache"
if os.name == 'nt': USERDATA = os.environ['APPDATA']
else:
    USERDATA = os.environ['HOME']
    FOLDERNAME = ".ThePiratePlayer"
    CACHEFOLDERNAME = ".cache"

# Folder Paths
USERDATA = os.path.join(USERDATA, FOLDERNAME)
DB_FOLDER = os.path.join(USERDATA, "DB")
CACHE_FOLDER = os.path.join(USERDATA, CACHEFOLDERNAME)

# If folders dont exist create them
if not os.path.exists(USERDATA): os.makedirs(USERDATA)
if not os.path.exists(DB_FOLDER): os.makedirs(DB_FOLDER)
if not os.path.exists(CACHE_FOLDER): os.makedirs(CACHE_FOLDER)