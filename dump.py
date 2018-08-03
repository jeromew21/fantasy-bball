from bs4 import BeautifulSoup
import requests
import os, time, json

from constants import *
from player import *

OFFLINE_PAGES = os.path.join("data", "bbref_cache")
PLAYERS_DATA = os.path.join("data", "players_data")

for path in (OFFLINE_PAGES, PLAYERS_DATA):
    if not os.path.isdir(path):
        os.makedirs(path)

URL_INDEX = os.path.join("data", "player_urls.txt")

def playerFromUrl(url, quiet=False):

    #on BBR, the table is commented out.. maybe to stop scrapers like me.
    if quiet:
        def print(*x):
            return None
    filename = os.path.join(OFFLINE_PAGES, url.split("/")[-1])
    print()
    try:
        with open(filename, "r") as f:
            html = f.read()
            f.close()
            print("Reading from file", filename)
    except:
        time.sleep(1) #in case of rate limiting
        html = requests.get(url).text
        html = html.replace('<!--', '<div>').replace('-->', '</div>') #fuck you!
        print("Falling back and downloading from URL", url)

    try:
        with open(filename , "w") as f:
            f.write(html)
            f.close()
        soup = BeautifulSoup(html, 'lxml')
        name = soup.find('h1', {'itemprop': 'name'}).contents[0]
        print("Parsing", name)
        player = Player(name)
        i = 0
        while i < 25:
            currentYear = LAST_YEAR - i
            tableRow = soup.find('tr', {'id': 'totals.{0}'.format(currentYear)})
            if tableRow:
                rowDict = {}
                for col in tableRow:
                    raw = col.contents
                    if len(raw) > 0:
                        raw = raw[0]
                        if raw.name in ('a', 'strong'):
                            raw = raw.contents[0]
                    else:
                        raw = 0
                    raw = str(raw)
                    try:
                        raw = float(raw)
                    except:
                        pass
                    rowDict[str(col['data-stat'])] = raw
                if rowDict:
                    rowDict['fg_pct'] = convertToContrib('fg', rowDict['fg'], rowDict['fga'])
                    rowDict['ft_pct'] = convertToContrib('ft', rowDict['ft'], rowDict['fta'])
                player.season_totals.append(rowDict)
            i += 1
        return player
    except Exception as e: 
        print("URL read from {0} ({1}) failed".format(name, url))
        print(str(e) + "\n")

def allPlayerUrls():
    with open(URL_INDEX, 'r') as f:
        return [url for url in f.read().split('\n') if url]

def downloadAll(cache_objects=True):
    urls = allPlayerUrls()
    for url in urls:
        player = playerFromUrl(url)
        if cache_objects:
            filename = os.path.join(PLAYERS_DATA, player.name.replace(" ", "-") + ".json")
            print("Saving object to", filename)
            f = open(filename, "w")
            f.write(json.dumps({
                "name": player.name,
                "season_totals": player.season_totals
            }))
            f.close()
            print("Saved object")

def allPlayers(cached=True):
    if cached:
        try:
            for k in os.listdir(PLAYERS_DATA):
                with open(os.path.join(PLAYERS_DATA, k)) as f:
                    js = f.read()
                    yield Player.from_json(js)
        except:
            print("Must rebuild player cache. Try running downloadAll()")
    else:
        for url in allPlayerUrls():
            yield playerFromUrl(url, quiet=True)

def listAllPlayers():
    return list(allPlayers())
