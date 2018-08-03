from dump import *
from functools import reduce
import numpy as np
import random

class Fantasy:
    def __init__(self):
        self.table = playerHashTable()
        self.players = listAllPlayers()
    def calc_avg(self, stat):
        if stat in CATEGORIES:
            return np.average(reduce(lambda x, y: x + y, [player.list_stat(stat) for player in self.players]))
    def random_player(self):
        return random.choice(self.players)

fan = Fantasy()
player = fan.random_player()
