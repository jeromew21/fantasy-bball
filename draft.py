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
        self.player_pool = self.sort(self.player_pool)

        self.drafted_players = []
        self.player_costs = self.estimate_costs()

        self.team = Team("my team")
    
    def sort(self, pool):
        return sorted(pool, key=lambda p: p.score, reverse=True)

    def show(self, count=15):
        self.estimate_costs(True, count)
    
    def show_drafted(self):
        i = 0
        for p in self.drafted_players:
            print(f"{i}. {p}")
            i += 1
    
    def undraft(self, i, cost):
        player = self.drafted_players.pop(i)
        print(f"Undrafting {player} for {cost}")
        self.player_pool.append(player)
        self.money_pool += cost

    def i_undraft(self, i, cost):
        player = self.drafted_players.pop(i)
        print(f"You undrafting {player} for {cost}")
        self.player_pool.append(player)
        self.money_pool += cost
        self.team.players.remove(player)
    
    def show_team(self):
        self.team.show()
    
    def i_draft(self, i, cost):
        player = self.player_pool.pop(i)
        print(f"You drafted {player} for ${cost}")
        self.team.add_player(player)
        self.drafted_players.append(player)
        self.money_pool -= cost
    
    def draft_player(self, i, cost):
        player = self.player_pool.pop(i)
        print(f"{player} drafted for ${cost}")
        self.drafted_players.append(player)
        self.money_pool -= cost

    def estimate_costs(self, verbose=False, shown=15):
        count = self.max_players_drafted - len(self.drafted_players)        
        players = self.player_pool[:count]
        economy = self.money_pool
        total_score = reduce(lambda x, y: x + y, [p.score for p in players])
        point_cost = economy / total_score        
        player_costs = [(p, int(p.score * point_cost)) for p in players]
        if verbose:
            print(f"Total score: {int(total_score)}")
            print(f"Total money: {int(economy)}")
            print("Cost per point: {0:.2f}".format(point_cost))
            print()
            i = 0
            for player, cost in player_costs[:shown]:
                print(f"{i}. {player}: ${cost}")
                i += 1
        return player_costs

def safe_input(s):
    while True:
        try:
            cmd = input(s)
            return cmd
        except (KeyboardInterrupt, EOFError):
            print()
            continue

def safe_to_int(s):
    try:
        k = int(s)
        return k
    except:
        return None

def frontend(d):
    print("Hello.")
    while True:
        cmd = safe_input("draft >>> ").split(" ")
        try:
            arg1 = cmd[0]
            arg2 = None
            arg3 = None
            arg4 = None
            if len(cmd) >= 2:
                arg2 = cmd[1]
            if len(cmd) >= 3:
                arg3 = cmd[2]
            if len(cmd) >= 4:
                arg4 = cmd[3]
        except:
            print("bad command")
            continue
        if arg1 in ('exit', 'quit', 'q'):
            if safe_input("Are you sure? >>> ")== "YES":
                sys.exit()
        elif arg1 in ('show', 'ls'):
            if arg2 is not None and arg2 in ("team", "me"):
                d.show_team()
            else:
                k = safe_to_int(arg2)
                if k:
                    d.show(k)
                else:
                    d.show()
        elif arg1 in ('i',) and arg2 in ("draft", "take"):
            index = safe_to_int(arg3)
            money = safe_to_int(arg4)
            if index is not None and money is not None:
                d.i_draft(index, money)
            else:
                print("Bad arguments")
        elif arg1 in ("draft",):
            index = safe_to_int(arg2)
            money = safe_to_int(arg3)
            if index is not None and money is not None:
                d.draft_player(index, money)
            else:
                print("Bad arguments")
        elif arg1 in ("shell", "drop"):
            while True:
                try:
                    code = input(">>> ")
                    if code in (
                        "quit",
                        "exit",
                        "exit()", 
                        "sys.exit()",
                    ):
                        break
                    print(eval(code))
                except (KeyboardInterrupt, EOFError):
                    print()
                    break
                except Exception as e:
                    print(f"Exception: {e}")
        elif arg1 in ("help",):
            print("Hahaha, you created this and you need help?")
        else:
            print("Not understood.")

    
if __name__ == "__main__":
    d = Draft()
    frontend(d)
        
