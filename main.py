from dsl.semantic import *
from dsl.parser import *
from dsl.hands import *
from model.match import *
import os
import settings
import logging


logging.basicConfig(level=logging.FATAL)
logging.info("Poker Analiser v{}".format(os.getenv("VERSION")))
logging.debug("Hand history at {}".format(os.getenv("HAND_HISTORY_PATH")))


histories = read_all_tournaments()

for history in histories:  # enumerable
    for hand in interpret(history):  # enumerable
        print(hand.actions)
