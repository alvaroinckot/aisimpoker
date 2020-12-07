from dsl.semantic import *
from dsl.parser import *
from dsl.hands import *
from model.match import *
from model.tournament import *
import os
import settings
import logging
import pandas as pd
from multiprocessing import Pool
import multiprocessing

logging.basicConfig(level=logging.FATAL)
logging.info("Poker Analyser v{}".format(os.getenv("VERSION")))
logging.debug("Hand history at {}".format(os.getenv("HAND_HISTORY_PATH")))


def do_the_magic(tournament_log):
    i = 1
    while (i <= 10):
        try:
            print("start")
            return interpret(tournament_log)
            break
        except Exception as ex:
            print(ex)
            if(i >= 10):
                print("MASTER FAILURE")
                return Tournament()
                break
            print("trying again for " + str(i))
            i += 1


if __name__ == '__main__':
    tournaments = read_all_tournaments()
    pre_flop_actions = []
    flop_actions = []
    turn_actions = []
    river_actions = []

    pool = Pool(os.cpu_count())
    results = pool.map(do_the_magic, tournaments)
    pool.close()
    pool.join()

    print("PROCESSANDO")
    for tournament in results:
        pre_flop_actions = pre_flop_actions + tournament.pre_flop_actions
        flop_actions = flop_actions + tournament.flop_actions
        turn_actions = turn_actions + tournament.turn_actions
        river_actions = river_actions + tournament.river_actions

    # save data
    path = "./compilations/summary_{}_v{}.csv"
    version = '14'

    if(len(pre_flop_actions) > 0):
        print("PROCESSANDO AGORA")

        pd.DataFrame(pre_flop_actions).fillna(0).to_csv(
            path.format("pre_flop", version), index=None, header=True)

        pd.DataFrame(flop_actions).fillna(0).to_csv(
            path.format("flop", version), index=None, header=True)

        pd.DataFrame(turn_actions).fillna(0).to_csv(
            path.format("turn", version), index=None, header=True)

        pd.DataFrame(river_actions).fillna(0).to_csv(
            path.format("river", version), index=None, header=True)
    else:
        print("actually I skipped for some reason")
