import sys

from fantasy import *
from teams import Team

class Draft:
    def __init__(self, num_teams=12, per_team=13, starting_money=200):
        self.num_teams = num_teams
        self.team_size = per_team
        self.money_pool = starting_money * num_teams
        self.max_players_drafted = num_teams * per_team

        self.player_pool = Fantasy().players
        self.drafted_players = []
        self.player_costs = self.estimate_costs()

        self.team = Team("my team")
    
    def show(self, count=15):
        self.estimate_costs(True, count)
    
    def show_team(self):
        self.team.show()
    
    def i_draft(self, i, cost):
        player = self.player_pool.pop(i)
        print(f"You drafted {player} for ${cost}")
        self.team.add_player(player)
        self.drafted_players.append(player)

    def estimate_costs(self, verbose=False, shown=15):
        players = self.player_pool
        economy = self.money_pool
        count = self.max_players_drafted - len(self.drafted_players)
        players = sorted(players, key=lambda p: p.score, reverse=True)[:count] #trim to exact num of players
        self.player_pool = players
        total_score = reduce(lambda x, y: x + y, [p.score for p in players])
        point_cost = economy / total_score        
        player_costs = [(p, int(p.score * point_cost)) for p in players]
        if verbose:
            print(f"Total score: {int(total_score)}")
            print(f"Total money: {int(economy)}")
            print(f"Cost per point: {int(point_cost)}")
            print()
            i = 0
            for player, cost in player_costs[:shown]:
                print(f"{i}. {player}: ${cost}")
                i += 1
        return player_costs

if __name__ == '__main__':
    print("Hello.")
    d = Draft()
    while True:
        try:
            cmd = input("draft >>> ").split(" ")
        except KeyboardInterrupt, EOFError:
            continue
        try:
            arg1 = cmd[0]
        except:
            print("bad command")
        
