
# The Pirate Player

- Simple script using IMDB API to get movies / tv shows.
- Sources: gomo.to, vidsrc.me
- I'm not responsible for any illegal usage of this script!
- Script made for educational / documentational purposes only!
## Installation

Install The Pirate Player with git

```bash
  git clone https://git.weboasis.app/HereIronman7746/ThePiratePlayer.git
  pip3 install -r requirements.txt
```
    
## Usage

### Settings
```bash
python3 settings.py set <key> <value>
```
All keys are in settings.py

### Running
```bash
python3 main.py
```
Then open ```http://ip:port/```

### M3U
This shit also has m3u support, you can create m3u by adding movies to playlist in /play/id.
```
http://ip:port/playlist.m3u
```

TV Shows have theire own m3u's which can be merged together.
```
http://ip:port/show/tt7286456.m3u
```

### Cache / Data
This shit stores cache and data in different directories based on os
- Linux: ```$home/.ThePiratePlayer```
- Win$hit: ```%appdata%\ThePiratePlayer```
## API Reference
Yeah, this also has api which can be accessed at /api/.
Here are some examples of best things it can do:

#### Resolve Item
```http
  GET /api/resolve/tt7286456
  GET /api/resolve/tt7286456?source=gomo / vidsrc
```
#### Poster
```http
  GET /api/poster/tt7286456
  GET /api/poster/tt7286456?do=show/redirect
```
#### IMDB Top / Bottom Movies
```http
  GET /api/top250movies/
  GET /api/bottom100movies/
```
## Contributing

You can contribute to this script at any time, idc

## Legal
For legal reasons:  
- I'm not associated with gomo.to / vidsrc.me / imdb.com / .. in ANY WAY  
- Script works by proxying these sites to get stream url  
- I CANNOT SHUT DOWN vidsrc / gomo I DONT OWN THEM  
- Address any legal shit to them, I can't do anything  
- I cannot be held responsible for piracy of gomo.to / vidsrc.me  
- I don't make any profits from this script nor do i track any data  
- I'm not responsible for any illegal usage of this script!  
- Script made for educational / documentational purposes only!  
- Do not share this script without appropriate credits  
- For IMDB API I use Cinemagoer  
- If you need more explaining how it works u can DM me here if it works or create issue  
- For any takedown requests create Issue  