LAST_YEAR = 2018

AVG_FG = 2272
AVG_FGA = 4966 #The average number of shots a fantasy team shoots per season.

AVG_FT = 1068
AVG_FTM = 1406

ALL_CATEGORIES = (
    'season',
    'age',
    'pos',
    'g',
    'gs',
    'mp',
    'fg',
    'fga',
    'fg_pct',
    'fg3',
    'fg3a',
    'fg3_pct',
    'fg2',
    'fg2a',
    'fg2_pct',
    'efg_pct',
    'ft',
    'fta',
    'ft_pct',
    'orb',
    'drb',
    'trb',
    'ast',
    'stl',
    'blk',
    'tov',
    'pf',
    'pts'
)

CATEGORIES = (
    'fg_pct', 
    'ft_pct',
    'pts', 
    'trb', 
    'ast', 
    'fg3', 
    'stl', 
    'blk',
    'tov'
)

def convertToContrib(t, makes, attempts):
    if t.lower() == 'fg':
        return (AVG_FG / AVG_FGA) - ((AVG_FG - makes) / (AVG_FGA  - attempts))
    return (AVG_FT / AVG_FTM) - ((AVG_FT - makes) / (AVG_FTM  - attempts))

def get_choice(arr):
    return arr[0]

reformats = {
    'fg_pct': "FG%",
    "ft_pct": "FT%",
    "fg3": "3PM",
    "trb": "REB"
}

def reformat_cat(c):
    if reformats.get(c.lower()):
        return reformats[c]
    return c.upper()

def suffix(x):
    lookup = {
        1: 'st',
        2: 'nd',
        3: 'rd'
    }
    return str(x) + lookup.get(x % 10, "th")
