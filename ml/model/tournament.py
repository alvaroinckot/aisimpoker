import numpy as np
from ml.model.match import *


class Tournament:
    def __init__(self):
        self.matches = []

    def start_new_match(self):
        self.matches.append(Match(len(self.matches) + 1))

    @property
    def current_match(self):
        return self.matches[-1]

    @property
    def pre_flop_actions(self):
        return sum([match.pre_flop_actions for match in self.matches], [])

    @property
    def flop_actions(self):
        return sum([match.flop_actions for match in self.matches], [])

    @property
    def turn_actions(self):
        return sum([match.turn_actions for match in self.matches], [])

    @property
    def river_actions(self):
        return sum([match.river_actions for match in self.matches], [])
