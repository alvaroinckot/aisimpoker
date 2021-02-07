from ml.dsl.semantic import *
from ml.dsl.parser import *
from ml.dsl.hands import *
from ml.model.match import *
from ml.model.tournament import *
import os
import settings
import logging
import pandas as pd

logging.basicConfig(level=logging.FATAL)
logging.info("Poker Analyser v{}".format(os.getenv("VERSION")))
logging.debug("Hand history at {}".format(os.getenv("HAND_HISTORY_PATH")))

pre_flop_actions, flop_actions, turn_actions, river_actions = [], [], [], []

for tournament_log in read_all_tournaments():  # enumerable
    tournament = interpret(tournament_log)
    pre_flop_actions = pre_flop_actions + tournament.pre_flop_actions
    flop_actions = flop_actions + tournament.flop_actions
    turn_actions = turn_actions + tournament.turn_actions
    river_actions = river_actions + tournament.river_actions


# save data
path = "./compilations/summary_{}_v{}.csv"
version = '999'

pd.DataFrame(pre_flop_actions).fillna(0).to_csv(
    path.format("pre_flop", version), index=None, header=True)

pd.DataFrame(flop_actions).fillna(0).to_csv(
    path.format("flop", version), index=None, header=True)

pd.DataFrame(turn_actions).fillna(0).to_csv(
    path.format("turn", version), index=None, header=True)

pd.DataFrame(river_actions).fillna(0).to_csv(
    path.format("river", version), index=None, header=True)
