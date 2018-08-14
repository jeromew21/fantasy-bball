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

def normalize(val, mean, sd):
    return float((val - mean) / sd)

class Player:
    def __init__(self, name):
        self.name = name
        self.season_totals = []
        self.last_year_zscore = {}
        self.last_year_totals = {}
        self.rank = None
        self.team = None
    
    def last_year_sigma(self, cat):
        if self.last_year_zscore:
            return self.last_year_zscore[cat]
        else:
            raise Exception("Improperly initialized player")

    def init_props(self, data):
        self.raw_score = self.calc_raw_score(data)

    @property
    def name_hash(self):
        """ Turn name into a hash for identification"""
        return abs(hash(self.name)) % (10 ** 6)

    @staticmethod
    def from_json(js):
        data = json.loads(js)
        player = Player(data['name'])
        player.season_totals = data['season_totals']
        player.team = data["current_team"]
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
    
    def calc_raw_score(self, data):
        """ Sum of total contributions, last season"""
        total = 0
        for stat_data in data:
            stat = stat_data["stat"]
            mean = stat_data["mean"]
            sd = stat_data["sd"]
            season_total = self.season_totals[0].get(stat, 0)
            score = normalize(season_total, mean, sd)
            self.last_year_zscore[stat] = score
            self.last_year_totals[stat] = season_total
            total += score
        return total
    
    def compare(self, other, data, dataset="last year"):
        """ Plots my zscore against another player's """
        mylabel = "{0} total: {1:.2f}".format(self, self.calc_raw_score(data))
        otherlabel = "{0} total: {1:.2f}".format(other, other.calc_raw_score(data))
        plot_title = '{} vs. {}, {}'.format(
            self, 
            other, 
            self.season_totals[0].get("season")
        )

        n_groups = 9
        if dataset == "last year":
            my_zscore = [self.last_year_zscore[stat] for stat in CATEGORIES]
            other_zscore = [other.last_year_zscore[stat] for stat in CATEGORIES]


        # create plot
        fig, ax = plt.subplots()
        index = np.arange(n_groups)
        bar_width = 0.35
        opacity = 0.8

        rects1 = plt.bar(index, my_zscore, bar_width,
                alpha=opacity,
                color='b',
                label=mylabel)

        rects2 = plt.bar(index + bar_width, other_zscore, bar_width,
                alpha=opacity,
                color='g',
                label=otherlabel)
        fig.canvas.set_window_title(plot_title)
        plt.ylabel('zscore σ')
        plt.xlabel('Category')
        plt.title(plot_title)
        plt.xticks(index + bar_width, (reformat_cat(c) for c in CATEGORIES))
        plt.legend(loc="upper left")

        plt.show()

    def plot_stat(self, stat):
        #Plots career trend for totals in cat
        pairs = [[int(year.get("season").split("-")[0]), float(year.get(stat, 0))] for year in self.season_totals]
        pairs = np.array(list(reversed(pairs)))
        print(pairs)
        x, y = pairs.T
        plt.title("{}".format(self))
        plt.xticks(x)
        plt.xlabel("Season")
        plt.ylabel(reformat_cat(stat))
        plt.plot(x, y, marker='o', markersize=3, color="red")
        plt.show()

    def plot_stats(self, stats=CATEGORIES):
        #Plots career trend for totals in (stats)
        years = np.array(list(reversed([int(year.get("season").split("-")[0]) for year in self.season_totals])))
        for stat in stats:
            s = np.array(list(reversed([float(year.get(stat, 0)) for year in self.season_totals])))
            print(s)
            plt.plot(years, s, marker='o', markersize=3, label=reformat_cat(stat))
        plt.xticks(years)
        plt.title("{} {}-cats".format(self, len(stats)))
        plt.xlabel("Season")
        plt.ylabel("Quantity")
        plt.legend(loc="upper left")
        plt.show()
    
    def plot_stats_normalized(self, data): # data is a list of [{stat:x, mean:x, sd:x}]
        
        ### Note on averages
        ### We can't take the league average of a category during a given season.
        ### Well, we could, but that would mean having to scrape the data
        ###     for all players during that period. 
        ### Instead, we'll just use the averages in TOTAL, for all the players we have.
        ### So this is ultimately flawed given the amount of scrub players in the data.

        years = list(reversed([int(year.get("season").split("-")[0]) for year in self.season_totals]))
        baseline = np.array([0 for i in years])
        years = np.array(years)

        plt.plot(years, baseline, label="League Average", linewidth=3, color="black")
        for stat_data in data:
            stat = stat_data["stat"]
            mean = stat_data["mean"]
            sd = stat_data["sd"]
            s = np.array(list(reversed([normalize(year.get(stat, 0), mean, sd) for year in self.season_totals])))
            print(s)
            plt.plot(years, s, marker='o', markersize=3, label=reformat_cat(stat))
        plt.xticks(years)
        plt.xlabel("Season")
        plt.ylabel("zscore")
        plt.title("{} 9-cats, Normalized".format(self))
        plt.legend(loc="upper left")
        plt.show()

    def __repr__(self):
        if self.rank:
            return "{} <{}> ({})".format(
                self.name, 
                self.name_hash,
                suffix(self.rank)
            )
        return "{} <{}>".format(self.name, self.name_hash)

    def __str__(self):
        return repr(self)