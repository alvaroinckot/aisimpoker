from dsl.semantic import *
from dsl.parser import *
from dsl.hands import *
from model.match import *
from model.tournament import *
import os
import settings
import logging
import pandas as pd

logging.basicConfig(level=logging.FATAL)
logging.info("Poker Analyser v{}".format(os.getenv("VERSION")))
logging.debug("Hand history at {}".format(os.getenv("HAND_HISTORY_PATH")))


tournaments = read_all_tournaments()
total = []

# todo -> parallelized map reduce

for tournament_log in tournaments:  # enumerable
    # try:
    tournament = interpret(tournament_log)  # enumerable
    total = total + tournament.actions
    print("tournament finished")
    break
    # except(e):
    # print("Something bad happened....")
    # continue


df = pd.DataFrame(total).fillna(0)
print(df)
# df.to_csv("./compilations/summary_v3.csv", index=None, header=True)
