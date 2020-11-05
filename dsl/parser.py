import os
from lark import Lark
import logging
from dsl.semantic import PokerSemantic
from dsl.hands import read_tournament
from model.match import *

logging.debug("Loading language syntax")
language = Lark.open('./dsl/poker.lark')
logging.debug("Finished loading language syntax")


def interpret(hand_history):
    hands = hand_history.split("\n\n\n")
    for hand in hands:
        tree = language.parse(hand)
        match = Match()
        semantic = PokerSemantic(match)
        semantic.transform(tree)
        yield match
