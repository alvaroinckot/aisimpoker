import os
from lark import Lark
import logging
from dsl.semantic import PokerSemantic
from dsl.hands import read_tournament

logging.debug("Loading language syntax")
language = Lark.open('./dsl/poker.lark')
logging.debug("Finished loading language syntax")


def interpret(hand_history, semantic=PokerSemantic()):
    hands = hand_history.split("\n\n\n")
    for hand in hands:
            tree = language.parse(hand)
            yield semantic.transform(tree)
