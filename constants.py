LAST_YEAR = 2018

AVG_FG = 2272
AVG_FGA = 4966

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

CATERGORIES = (
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
    