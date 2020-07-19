from dsl.semantic import *
from dsl.parser import *
from dsl.hands import *
import os
import settings
import logging


logging.basicConfig(level=logging.FATAL)
logging.info("Poker Specialist v{}".format(os.getenv("VERSION")))
logging.debug("Hand history at {}".format(os.getenv("HAND_HISTORY_PATH")))


histories = read_all_tournaments()

semantic = PokerSemantic()

for history in histories:  # enumerable
    for hand in interpret(history, semantic=semantic):  # enumerable
        print(hand)
        input()
