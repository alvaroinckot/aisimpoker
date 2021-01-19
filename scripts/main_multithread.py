import traceback
import tqdm
import multiprocessing
from multiprocessing import Pool
import pandas as pd
import logging
import settings
import os

from ml.model.tournament import *
from ml.model.match import *
from ml.dsl.hands import *
from ml.dsl.parser import *
from ml.dsl.semantic import *

logging.basicConfig(level=logging.FATAL)
logging.info("Poker Analyser v{}".format(os.getenv("VERSION")))
logging.debug("Hand history at {}".format(os.getenv("HAND_HISTORY_PATH")))


def do_the_magic(tournament_log):
    try:
        return interpret(tournament_log)
    except Exception as ex:
        traceback.print_exc()
        # print(tournament_log)


if __name__ == '__main__':
    number_of_tournaments = len(list_tournament_files())
    tournaments = read_all_tournaments()
    pre_flop_actions = []
    flop_actions = []
    turn_actions = []
    river_actions = []

    pool = Pool(os.cpu_count())
    # results = pool.map(do_the_magic, tournaments)
    results = [x for x in tqdm.tqdm(pool.imap_unordered(
        do_the_magic, tournaments), total=number_of_tournaments)]

    pool.close()
    pool.join()

    for tournament in results:
        if(tournament == None):
            continue
        pre_flop_actions = pre_flop_actions + tournament.pre_flop_actions
        flop_actions = flop_actions + tournament.flop_actions
        turn_actions = turn_actions + tournament.turn_actions
        river_actions = river_actions + tournament.river_actions

    # save data
    path = "./compilations/summary_{}_v{}.csv"
    version = '21'

    if(len(pre_flop_actions) > 0):

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
