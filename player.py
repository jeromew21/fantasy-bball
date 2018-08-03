import json

class Player:
    def __init__(self, name):
        self.name = name
        self.season_totals = []

    @property
    def name_hash(self):
        """ Turn name into a hash for identification"""
        return 0

    @staticmethod
    def from_json(js):
        data = json.loads(js)
        player = Player(data['name'])
        player.season_totals = data['season_totals']
        return player
    
    def show(self):
        for year in self.season_totals():
            print(year)

    def __repr__(self):
        return "{} <{}>".format(self.name, self.name_hash)
