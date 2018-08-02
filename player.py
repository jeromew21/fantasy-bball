import json

class Player:
    def __init__(self, name):
        self.name = name
        self.season_totals = []

    @staticmethod
    def from_json(js):
        data = json.loads(js)
        player = Player(data['name'])
        player.season_totals = data['season_totals']
        return player