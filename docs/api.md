# API Reference


## Get server status
```
GET /api/
```
#### Response Example
```json
{
    'status': 'ok',
    'message': 'API Running'
}
```

---

## Get featured movie
```
GET /api/featured'
```
#### Response Example
```json
{
    "img": "/api/banner/tt7286456?do=show",
    "title": "JOKER",
    "line": "SMILE AND PUT ON A HAPPY FACE",
    "info": "8.4/10\u00A0\u00A02019\u00A0\u00A0Crime, Drama, Thriller\u00A0\u00A02h 20m",
    "plot": "A socially inept clown for hire - Arthur Fleck aspires to be a stand up comedian among his small job working dressed as a clown holding a sign for advertising. He takes care of his mother- Penny Fleck, and as he learns more about his mental illness, he learns more about his past. Dealing with all the negativity and bullying from society he heads downwards on a spiral, in turn showing how his alter ego \"Joker\", came to be.",
	"imdbID": "tt7286456",
	"kind": "movie",
    "inPlaylist": true,
    "inFavorites: true
}
```

---
## Get home categories
```
GET /api/homeMenu
```
#### Response Example
```json
[
  {
    "title": "Action",
    "url": "/api/getMoviesByGenres?genres=Action",
    "enabled": false
  },
  {
    "title": "Adventure",
    "url": "/api/getMoviesByGenres?genres=Adventure",
    "enabled": false
  }
]
```

---
## Get default home options
```
GET /api/defaultHome
```
#### Response Example
```json
[
  {
    "title": "Action",
    "url": "/api/getMoviesByGenres?genres=Action",
    "enabled": true
  },
  {
    "title": "Adventure",
    "url": "/api/getMoviesByGenres?genres=Adventure",
    "enabled": true
  }
]
```

---
## Get IP used for grabbing
```
GET /api/requestsIP
```
#### Response Example
```
1.1.1.1
```

---
## Set new home items
```
GET /api/updateHomeMenu?new=base64encoded json
```
#### Response Example
```
Done / Error
```

---
## Exec command in CLI
```
GET /api/terminal
```
#### Response Example
```
Command response
```

---
## Get userdata (Hides password, history, favorites, playlist from response)
```
GET /api/userInfo
```
#### Response Example
```json
{
  "UID": "w26r660jvu6dbvp6msik7hlmln1thiuavzuyqhzkhplhv4ctspyb9bqci9xyjym8",
  "username": "admin",
  "isAdmin": true,
  "email": "",
  "home" : [],
  "createdOn": 1669898124,
  "isBanned": false,
  "ip": "Disabled"
}

```

---
## Get all registered users
```
GET /api/users
```
#### Response Example
```json
{
  "w26r660jvu6dbvp6msik7hlmln1thiuavzuyqhzkhplhv4ctspyb9bqci9xyjym8": {
    "UID": "w26r660jvu6dbvp6msik7hlmln1thiuavzuyqhzkhplhv4ctspyb9bqci9xyjym8",
    "username": "admin",
    "isAdmin": true,
    "isBanned": false,
    "ip": "Disabled",
    "email": ""
  }
}
```

---
## Make admin / remove admin
```
GET /api/promoteDemote/<uid>
```
#### Response Example
```
Done
```

---
## Ban / Unban
```
GET /api/banUnban/<uid>
```
#### Response Example
```
Done
```

---
## Delete user
```
GET /api/deleteUser/<uid>
```
#### Response Example
```
Done
```

---
## Change password
```
GET /api/changePassword/<uid>/<new password>
```
#### Response Example
```
Done
```

---
## Resolve Movie item
```
GET /api/resolve/<imdb id>?source=src
GET /api/resolve/<imdb id>?source=src&episode=1-1
```
#### Response Example
```json
{
    "id": id,
    "url": "Resolved url"
}
```

---
## Get sources
```
GET /api/sources/<imdb id>?source=src&kind=movie
GET /api/sources/<imdb id>?source=src
```
#### Response Example
```json
[
    {
        "title": "Title",
        "file": "Resolved url"
    }
]
```

---
## Get poster
```
GET /api/poster/<imdb id>?do=show/redirect
```
#### Response Example
```
Image / Redirect
```

---
## Get banner
```
GET /api/banner/<imdb id>?do=show/redirect
```
#### Response Example
```
Image / Redirect
```

---
## Search for movies / tvshows
```
GET /api/search/<query>
```
#### Response Example
```json
{
    "query": query,
    "results": {
        "tt10999120": {
            "title": "Spirited",
            "kind": "movie",
            "id": "tt10999120",
            "poster": "/api/poster/tt10999120?do=show"
        }
    }
}
```

---
## Get seasons
```
GET /api/seasons/<imdb id>
```
#### Response Example
```json
{
    "query": query,
    "results": {}
}
```

---
## Get episodes
```
GET /api/episodes/<imdb id>/<season>
```
#### Response Example
```json
{
    "query": query,
    "results": {}
}
```

---
## Get episode count for all seasons
```
GET /api/episodeCount/<imdb id>
```
#### Response Example
```json
{
    "query": query,
    "results": {}
}
```

---
## IMDB Top 250 movies
```
GET /api/top250movies/
```
#### Response Example
```json
{
    "query": query,
    "results": {}
}
```

---
## IMDB Bottom 100 movies
```
GET /api/bottom100movies/
```
#### Response Example
```json
{
    "query": query,
    "results": {}
}
```

---
## Get movies by genre/s
```
GET /api/getMoviesByGenres?genres=Action|Family
```
#### Response Example
```json
{
    "query": query,
    "results": {}
}
```

---
## Proxy
```
GET /api/proxy/<url>
```
#### Response Example
```
Data
```

---
## Get movie info
```
GET /api/getMovieInfo/<imdb id>
```
#### Response Example
```json
{
  "title": "Scream",
  "plot": "25 years after a streak of brutal murders shocked the quiet town of Woodsboro, Calif., a new killer dons the Ghostface mask and begins targeting a group of teenagers to resurrect secrets from the town's deadly past.",
  "poster": "https://m.media-amazon.com/images/M/MV5BYjExYTcwYmYtMWY2Zi00MGJlLTk3YjUtZTU1Zjg4MDc0Y2FjXkEyXkFqcGdeQXVyODE5NzE3OTE@.jpg",
  "year": 2022,
  "genres": "Horror, Mystery, Thriller",
  "episodeCount": "0",
  "airDate": "03 Feb 2022 (Country)",
  "rating": 6.3,
  "budget": "$24,000,000 (estimated)",
  "info": "6.3/10\u00a0\u00a02022\u00a0\u00a0Horror, Mystery, Thriller\u00a0\u00a01h 54m",
  "kind": "movie",
  "inFavorites": false,
  "inPlaylist": false
}

```