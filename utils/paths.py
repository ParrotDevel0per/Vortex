import os

USERDATA = ""
FOLDERNAME = "Vortex"
CACHEFOLDERNAME = "cache"
if os.name == 'nt': USERDATA = os.environ['APPDATA']
else:
    USERDATA = os.environ['HOME']
    FOLDERNAME = ".Vortex"
    CACHEFOLDERNAME = ".cache"

# Folder Paths
USERDATA = os.path.join(USERDATA, FOLDERNAME)
DB_FOLDER = os.path.join(USERDATA, "DB")
CACHE_FOLDER = os.path.join(USERDATA, CACHEFOLDERNAME)
POSTER_FOLDER = os.path.join(USERDATA, "posters")
BANNER_FOLDER = os.path.join(USERDATA, "banners")

# If folders dont exist create them
if not os.path.exists(USERDATA): os.makedirs(USERDATA)
if not os.path.exists(DB_FOLDER): os.makedirs(DB_FOLDER)
if not os.path.exists(CACHE_FOLDER): os.makedirs(CACHE_FOLDER)
if not os.path.exists(POSTER_FOLDER): os.makedirs(POSTER_FOLDER)
if not os.path.exists(BANNER_FOLDER): os.makedirs(BANNER_FOLDER)