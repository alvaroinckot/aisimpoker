from dsl.semantic import *
from dsl.parser import *
from dsl.hands import *
from model.match import *
import os
import settings
import logging
import pandas as pd

logging.basicConfig(level=logging.FATAL)
logging.info("Poker Analiser v{}".format(os.getenv("VERSION")))
logging.debug("Hand history at {}".format(os.getenv("HAND_HISTORY_PATH")))


histories = read_all_tournaments()
total = []

for history in histories:  # enumerable
    for hand in interpret(history):  # enumerable
        # https://github.com/ihendley/treys/blob/master/treys/card.py
        print(hand.id)  # should consolidate to a csv
        total = total + hand.actions


df = pd.DataFrame(total).fillna(0)
print(df)
df.to_csv("./compilations/summary_v1.csv", index=None, header=True)
