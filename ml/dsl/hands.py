import os
from lark import Lark
import logging

# todo move to another folder, this does not belongs to this module


def list_tournament_files(dir=os.getenv("HAND_HISTORY_PATH")):
    return os.listdir(dir)


def read_tournament(dir=os.getenv("HAND_HISTORY_PATH"), tournament_file):
    path = "{}/{}".format(dir, tournament_file)
    with open(path, 'r', encoding=os.getenv("HAND_HISTORY_ENCODE")) as file:
        return file.read().replace("/n/n/n", "")


def read_all_tournaments(dir=os.getenv("HAND_HISTORY_PATH")):
    for tournament_file in list_tournament_files(dir):
        yield read_tournament(dir, tournament_file)
