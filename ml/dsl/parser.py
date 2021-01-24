import os
from lark import Lark
import logging
from ml.dsl.semantic import PokerSemantic
from ml.dsl.hands import read_tournament
from ml.model.tournament import Tournament

logging.debug("Loading language syntax")
language = Lark.open('./ml/dsl/poker.lark')
logging.debug("Finished loading language syntax")


def interpret(hand_history):
    tree = language.parse(hand_history)
    tournament = Tournament()
    semantic = PokerSemantic(tournament)
    semantic.transform(tree)
    return tournament
