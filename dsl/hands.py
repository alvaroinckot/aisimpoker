import os
from lark import Lark
import logging

# todo move to another folder, this does not belongs to this module


def list_tournament_files():
    return os.listdir(os.getenv("HAND_HISTORY_PATH"))


def read_tournament(tournament_file):
    path = "{}/{}".format(os.getenv("HAND_HISTORY_PATH"), tournament_file)
    with open(path, 'r', encoding=os.getenv("HAND_HISTORY_ENCODE")) as file:
        return file.read().replace("/n/n/n", "")


def read_all_tournaments():
    for tournament_file in list_tournament_files():
        yield read_tournament(tournament_file)
