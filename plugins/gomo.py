import requests
import re
from utils.unpacker import unpack

useALT = False

def getParts(url):
    html = requests.get(url).text
    try:
        tc = re.findall(r"var tc = '(.*?)';", html)[0]
    except:
        raise Exception(html)
    _token = html.replace("\n", "").split("_token\": \"")[1].split("\",")[0]
    sliceF = re.search(r"slice\((.*?)\)", html).group(1)
    matches = re.search(r"\) \+ \"(.*?)\"\+\"(.*?)\";", html)
    return tc, _token, matches, sliceF

def fuckToken(token, matches, slices):
    slices = slices.split(",")
    return token[int(slices[0]):int(slices[1])][::-1] + str(eval(matches.group(1) + matches.group(2)))

def getSources(url):
    tc, _token, matches, slices = getParts(url)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    headers.update({"x-token": fuckToken(tc, matches, slices)})
    data = {"tokenCode": tc, "_token": _token}
    resp = requests.post("https://gomo.to/decoding_v3.php", headers=headers, data=data, allow_redirects=True)
    sources = eval(resp.text.replace('\/', '/'))
    return list(set([source for source in sources if "gomo" in source]))

def grab(url):
    sources = getSources(url)
    if useALT:
        url = [source for source in sources if "vid1" in source][0]
        resp = requests.get(url).text
        mirrorServer = "http:" + re.search(r'<a href="(.*?)"><li>Mirror Server</li></a>', resp).group(1)
        resp = requests.get(mirrorServer).text
    try:
        resp = requests.get(sources[0]).text
        packed = resp.replace("\n", "").split("<script type='text/javascript'>")[1].split("</script>")[0]
    except Exception as e:
        #print(e)
        #print("Source #1 failed, trying source #2")
        resp = requests.get(sources[1]).text
        packed = resp.replace("\n", "").split("<script type='text/javascript'>")[1].split("</script>")[0]
    unpacked = unpack(packed)
    if requests.get(unpacked.split("$.get('")[1].split("'")[0] + "1").text != "1": print("", end="") #print("Error might occur")
    unpacked = unpacked.split("[")[1].split("]")[0]
    try:
        m3u8Source = f'http{re.search(r"http(.*?)m3u8", unpacked).group(1)}m3u8'
        return m3u8Source
    except Exception as e: pass
    try:
        mp4Sources = [f'http{source}mp4' for source in re.findall(r"http(.*?)mp4", unpacked.replace(m3u8Source, ""))]
    except Exception as e:
        mp4Sources = [f'http{source}mp4' for source in re.findall(r"http(.*?)mp4", unpacked)]
    labelsDef = re.findall(r'label:"(.*?)"', unpacked)
    labels = []
    for label in labelsDef:
        if len(label) == 6:
            firstPart = label[:3]
            secondPart = label[3:]
            labels.append(f"{firstPart}x{secondPart}")
        else: labels.append(label)
    return mp4Sources[0]
