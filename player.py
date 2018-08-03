import json
from constants import *
import matplotlib.pyplot as plt
import numpy as np

def truncate(s, n):
    chop = str(s)[:n]
    if len(chop) < n:
        missing = n - len(chop)
        chop = missing * " " + chop
    if chop.endswith(".0"):
        chop = "  " + chop[0:-2]
    if chop[-1] == ".":
        chop = " " + chop[0:-1]
    return chop

class Player:
    def __init__(self, name):
        self.name = name
        self.season_totals = []

    @property
    def name_hash(self):
        """ Turn name into a hash for identification"""
        return abs(hash(self.name)) % (10 ** 6)

    @staticmethod
    def from_json(js):
        data = json.loads(js)
        player = Player(data['name'])
        player.season_totals = data['season_totals']
        return player
    
    def list_stat(self, stat): 
        """ Return a list of values of stat for each season played. """
        return [y.get(stat, 0) for y in self.season_totals]

    def show(self):
        print("{} ({})\n".format(self.name_hash, self.name))
        rows = ("season", "age", "mp") + CATEGORIES
        for stat in rows:
            print(truncate(stat, 4), end="|")
        print()
        for year in self.season_totals:
            for stat in rows:
                value = year[stat]
                if stat in ('fg_pct', 'ft_pct'):
                    value = value * 100
                print(truncate(value, 4), end="|")
            print()
    
    def plot_stat(self, stat):
        pairs = [[int(year.get("season").split("-")[0]), float(year.get(stat, 0))] for year in self.season_totals]
        pairs = np.array(list(reversed(pairs)))
        print(pairs)
        x, y = pairs.T
        plt.title("{} {}".format(self))
        plt.xticks(x)
        plt.plot(x, y, marker='o', markersize=3, color="red")
        plt.show()

    def plot_stats(self, stats=CATEGORIES):
        years = np.array(list(reversed([int(year.get("season").split("-")[0]) for year in self.season_totals])))
        for stat in stats:
            s = np.array(list(reversed([float(year.get(stat, 0)) for year in self.season_totals])))
            print(s)
            plt.plot(years, s, marker='o', markersize=3)
        plt.xticks(years)
        plt.title("{} {}-cat".format(self, len(stats)))
        plt.show()


    def __repr__(self):
        return "{} <{}>".format(self.name, self.name_hash)

    def __str__(self):
        return repr(self)