import random
import numpy as np
import matplotlib.pyplot as plt

from constants import *
from fantasy import *

class Team:
    SIZE = 13
    def __init__(self, name):
        self.name = name
        self.players = []
        self.week_wins = 0
        self.week_losses = 0
        self.week_ties = 0
        self.category_record = {}
        for c in CATEGORIES:
            self.category_record[c] = {
                "wins": 0, "losses": 0
            }
        self.lg =  None
    
    @property
    def winning_percentage(self):
        try:
            pct = 100 * (self.week_wins 
                / (self.week_losses + self.week_wins + self.week_ties))
        except:
            print("No games played")
        else:
            return "{:.2f}".format(pct)
    
    def show(self, verbose=False):
        print(self.name)
        print(", ".join([str(p) for p in self.players]))
        if verbose:
            print("Wins: {}".format(self.week_wins))
            print("Losses: {}".format(self.week_losses))
            print("Win Pct: {}".format(self.winning_percentage))
        x = CATEGORIES
        y = [
            self.score(cat)
            for cat in x
        ]
        plt.bar(x, y)
        plt.title("{}'s Team Attributes (z-scores)".format(self.name))
        plt.show()
    
    def _add_player(self, p):
        self.players.append(p)
    
    def score(self, cat):
        return sum(p.last_year_sigma(cat) for p in self.players)
    
    def play(self, oppo):
        cats = 0
        for cat in CATEGORIES:
            if (sum(p.last_year_sigma(cat) for p in self.players)
               > sum(p.last_year_sigma(cat) for p in oppo.players)):
                #if starts here
                cats += 1
                self.category_record[cat]["wins"] += 1
                oppo.category_record[cat]["losses"] += 1
            else:
                self.category_record[cat]["losses"] += 1
                oppo.category_record[cat]["wins"] += 1
        if cats > 4:
            self.week_wins += 1
            oppo.week_losses += 1
        else:
            self.week_losses += 1
            oppo.week_wins += 1
    
    def add_player_by_name(self, name):
        player = self.lg.fan.search(name)
        if player:
            self._add_player(player)
            self.lg.fan.players.remove(player)
            return True
        return False
    
    def add_player(self, p):
        self._add_player(p)

class League:
    def __init__(self):
        self.fan = Fantasy()
        self.fan.sort_by_raw(show=False)
        self.teams = []
    def add_team(self, t):
        t.lg = self
        self.teams.append(t)
    def randomly_populate(self, count):
        pool = count * Team.SIZE
        players = self.fan.sort_by_raw(limit=pool, show=False)
        random.shuffle(players)
        new_teams = []
        for i in range(count):
            new_teams.append(Team("Team {}".format(i + 1)))
        for team in new_teams:
            for _ in range(Team.SIZE):
                team._add_player(players.pop())
        self.teams.extend(new_teams)
    def sim(self):
        for team in self.teams:
            for oppo in self.teams:
                if team is not oppo:
                    team.play(oppo)
            

if __name__ == "__main__":
    lg = League()
    team = Team("Jerome's Cool Team")
    lg.add_team(team)
    team.add_player_by_name("Paul George")
    team.add_player_by_name("LeBron")
    team.add_player_by_name("Stephen")
    team.add_player_by_name("Klay")
    team.add_player_by_name("Thaddeus")
    team.add_player_by_name("Kyle L")
    team.add_player_by_name("Lauri")
    team.add_player_by_name("Jayson T")
    team.add_player_by_name("Enes K")
    team.add_player_by_name("Andre Ig")
    team.add_player_by_name("Draymond")
    team.add_player_by_name("Zaza Pa")
    lg.randomly_populate(7)
    lg.sim()
    n = 10000
    for i in reversed(range(n)):
        lg.teams = [team]
        lg.randomly_populate(7)
        lg.sim()
        print("simming {}".format(i))
    team.show()
    