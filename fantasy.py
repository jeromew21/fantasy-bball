from dump import *
from constants import *
from functools import reduce
import numpy as np
import matplotlib.pyplot as plt
import random

class Fantasy:
    def __init__(self):
        self.players = [p for p in allPlayers() if len(p.season_totals) > 0]

        self.stat_data = [{
            "stat": stat,
            "mean": self.calc_avg(stat),
            "sd": self.calc_sd(stat)
        } for stat in CATEGORIES]
        
        self.teams = {}

        for p in self.players:
            p.init_props(self.stat_data)
            team = p.team
            if team:
                if team in self.teams:
                    self.teams[team].append(p)
                else:
                    self.teams[team] = [p]
        self.table = playerHashTable(self.players)

    def all_stat_values(self, stat):
        return reduce(lambda x, y: x + y, [player.list_stat(stat) for player in self.players])
    
    def calc_avg(self, stat, lastYear=True):
        if lastYear:
            np.average([p.last_year_totals.get(stat, 0) for p in self.players])
        # Using ALL years might yield a more accurate average
        return np.average(self.all_stat_values(stat))
    
    def calc_sd(self, stat, lastYear=True):
        if lastYear:
            np.std([p.last_year_totals.get(stat, 0) for p in self.players])
        return np.std(self.all_stat_values(stat))
    
    def depth_chart(self, team_name):
        team = self.teams.get(team_name)
        team = sorted(team, key=lambda player: player.raw_score, reverse=True)
        for p in team:
            print(p)

    def random_player(self):
        return random.choice(self.players)

    def search(self, query):
        possible = [p for p in self.players if p.name.lower().startswith(query.lower())]
        if not possible:
            print("No player matching that search")
            return None
        return get_choice(possible)

    def sort_by(self, func):
        return sorted(self.players, key=func)

    def sort_by_raw(self, limit=100, show=True):
        result = []
        i = 1
        for p in reversed(self.sort_by(lambda player: player.raw_score)):
            p.rank = i
            if i <= limit:
                result.append(p)
                if show:
                    print("{}. {}".format(i, p))
            i += 1
        return result

    def histogram(self, stat="total", limit=144):
        if stat == "total":
            v = np.array([p.raw_score for p in self.players[:limit]])
        else:
            v = np.array([p.last_year_zscore[stat] for p in self.players[:limit]])
        plt.hist(v, bins=25)
        plt.title("{} {} distribution".format(
                stat, 
                "sum z-scores" if stat == "total" else "z-score"
            )
        )
        plt.show()

    def compare_last_year(self, p1, p2):
        assert isinstance(p1, Player) and isinstance(p2, Player)
        p1.compare(p2, self.stat_data, "last year")
    

fan = Fantasy()
player = fan.random_player()
