import numpy as np
from model.match import *


class Tournament:
    def __init__(self):
        self.matches = []

    def start_new_match(self):
        self.matches.append(Match(len(self.matches)))

    @property
    def current_match(self):
        return self.matches[-1]

    @property
    def actions(self):
        return sum([match.actions for match in self.matches], [])
