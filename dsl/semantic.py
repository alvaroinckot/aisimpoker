from lark import Lark, Transformer, v_args, Tree
from model.tournament import Tournament
import ast


class PokerSemantic(Transformer):

    def __init__(self, tournament_model):
        self._tournament = tournament_model
        self._tournament.start_new_match()

    def game(self, token):
        self._tournament.start_new_match()
        return None

    def hand(self, token):
        self._tournament.current_match.id = ast.literal_eval(token[0])

    def player(self, token):
        return token[0].strip()

    def received_card(self, token):
        self._tournament.current_match.set_hero(token[0])
        self._tournament.current_match.set_hand_card(token[1].children)

    def chips(self, token):
        return ast.literal_eval(token[0])

    def seat(self, token):
        seat = {'name': token[1], 'chips': token[2], 'seat': ast.literal_eval(
            token[0]),  'is_out': (len(token) == 4 and token[3].type == "IS_OUT")}
        self._tournament.current_match.seats.append(seat)
        return seat

    def blind(self, token):
        self._tournament.current_match.blind = ast.literal_eval(token[2])

    def ante(self, token):
        self._tournament.current_match.pot += ast.literal_eval(token[1])

    def small_blind(self, token):
        self._tournament.current_match.small_blind_player = token[0]
        self._tournament.current_match.pot += ast.literal_eval(token[1])

    def big_blind(self, token):
        self._tournament.current_match.big_blind_player = token[0]
        self._tournament.current_match.pot += ast.literal_eval(token[1])

    def pre_flop(self, token):
        for action in token:
            if(action.children[0] != None):
                self._tournament.current_match.add_pre_flop_action(
                    action.children[0])

    def flop(self, token):
        self._tournament.current_match.set_board_cards(token[1].children)
        for action in token[2:]:
            if(action.children[0] != None):
                self._tournament.current_match.add_flop_action(
                    action.children[0])

    def turn(self, token):
        self._tournament.current_match.set_board_cards(token[2].children)
        for action in token[3:]:
            if(action.children[0] != None):
                self._tournament.current_match.add_turn_action(
                    action.children[0])

    def river(self, token):
        self._tournament.current_match.set_board_cards(token[2].children)
        for action in token[3:]:
            if(action.children[0] != None):
                self._tournament.current_match.add_river_action(
                    action.children[0])

    def raised(self, token):
        return {'action': 'raise', 'player': token[0], 'action_chips': ast.literal_eval(token[1])}

    def bet(self, token):
        return {'action': 'raise', 'player': token[0], 'action_chips': ast.literal_eval(token[1])}

    def fold(self, token):
        return {'action': 'fold', 'player': token[0], 'action_chips': 0}

    def call(self, token):
        return {'action': 'call', 'player': token[0], 'action_chips': ast.literal_eval(token[1])}

    def check(self, token):
        return {'action': 'check', 'player': token[0], 'action_chips': 0}

    def timeout(self, token):
        return {'action': 'timeout', 'player': token[0], 'action_chips': 0}

    def card(self, token):
        return {'value': token[0].value, 'suit': token[1].value}

    def uncalled_bet(self, token):
        return None

    def prize_collect_hand(self, token):
        return None

    def hide_hand(self, token):
        return None

    def timeout_disconnected(self, token):
        return None

    def disconnected(self, token):
        return None

    def connected(self, token):
        return None

    def chat(self, token):
        return None

    def returned(self, token):
        return None

    def is_sitting_out(self, token):
        self._tournament.current_match.opponents_sitting_out += 1

    def show_down_player(self, token):
        return None
