from bs4 import BeautifulSoup
import requests

ROOT_URL = 'https://www.basketball-reference.com'
LAST_YEAR = 2018
LOG_FILE = 'log.txt'

class League:
    def __init__(self):
        self.teams = []

class Team:
    def __init__(self):
        self.roster = []

class Player:
    def __init__(self, name):
        print("Created {0}.".format(name))
        self.name = name
        self.totals = [{}, {}, {}]
    @property
    def lastYearTotals(self):
        return self.totals[0]
    def __str__(self):
        return 'Player {0}'.format(self.name)

def playerFromURL(url):
    try:
        #on BBR, the table is commented out.. maybe to stop scrapers like me.
        html = requests.get(url).text.replace('<!--', '<div>').replace('--!>', '</div>') #fuck you!
        soup = BeautifulSoup(html, 'lxml')
        name = soup.find('h1', {'itemprop': 'name'}).contents[0]
        p = Player(name)
        lastYearRow = soup.find('tr', {'id': 'totals.{0}'.format(LAST_YEAR)})
        for col in lastYearRow:
            contents = col.contents[0]
            if contents.name == 'a':
                contents = contents.contents[0]
            p.lastYearTotals[col['data-stat']] = contents
        print(p.lastYearTotals)
        with open('players/{0}.txt'.format(name), 'w') as f:
            f.write(str(lastYearRow))
            f.close()
        return p
    except: 
        log("URL read from {0} failed".format(url))

def parseFile(path):
    result = []
    with open(path, 'r') as f:
        result = f.read().split('\n')
    return result

def getAllActivePlayerURLS():
    alph = 'abcdefghijklmnopqrstuvwxyz'
    baseurl = ROOT_URL + '/players/{0}/'
    letterPages = [baseurl.format(ch) for ch in alph]
    names = []
    urls = []
    for url in letterPages:
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
        for link in soup.find_all('a'):
            if link.parent.name == 'strong':
                print(link.contents[0])
                names.append(link.contents[0])
                urls.append(ROOT_URL + link['href'])
    with open('names.txt', 'w') as f:
        f.write('\n'.join(names))
        f.close()
    with open('playerURLs.txt', 'w') as f:
        f.write('\n'.join(urls))
        f.close()
    return urls

def log(l):
    with open(LOG_FILE, "a") as f:
        f.write("\n" + l)
        f.close()
    print("Wrote", l, "to log")

def allPlayers():
    result = []
    urls = parseFile("playerURLs.txt")
    for url in urls:
        result.append(playerFromURL(url))
    return result

def debug():
    playerFromURL(parseFile("playerURLs.txt")[45])