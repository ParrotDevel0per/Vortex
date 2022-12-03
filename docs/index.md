# Vortex
Media center coded in python and javascript

## Installation
There is currently only one way to install Vortex

#### GIT
```bash
git clone https://git.weboasis.app/HereIronman7746/Vortex.git
cd Vortex
virtualenv -p python3 venv
```

Linux:  
```bash
source venv/bin/activate
```

Windows (powershell):  
```bash
.\venv\Scripts\activate
```

Then install dependencies
```bash
pip install -r requirements.txt
```

## Running
Run with python:
```bash
python3 main.py
```

Optional arguments:
- ```--cli``` - Autostart CLI  
- ```--nocli``` - Do not ask for cli  
- ```--debug``` - Run Vortex with flask debug  
  