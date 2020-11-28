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

    # def total_pot(self, token):
        # print(token[0])

    def seat(self, token):
        seat = {'name': token[1], 'chips': token[2], 'seat': ast.literal_eval(
            token[0]),  'is_out': (len(token) == 4 and token[3].type == "IS_OUT")}
        self._tournament.current_match.seats.append(seat)
        return seat

    def blind(self, token):
        self._tournament.current_match.blind = ast.literal_eval(token[2])

    # def _street_call(self, street, token):
    #     for action in token:
    #         if(action.children[0] != None):
    #             self._tournament.current_match.add_player_action(
    #                 street, action.children[0])

    def pre_flop(self, token):
        for action in token:
            if(action.children[0] != None):
                self._tournament.current_match.add_pre_flop_action(
                    action.children[0])

    def flop(self, token):
        for action in token[2:]:
            if(action.children[0] != None):
                self._tournament.current_match.add_flop_action(
                    action.children[0])

    def turn(self, token):
        for action in token[3:]:
            if(action.children[0] != None):
                self._tournament.current_match.add_turn_action(
                    action.children[0])

    def river(self, token):
        for action in token[3:]:
            if(action.children[0] != None):
                self._tournament.current_match.add_river_action(
                    action.children[0])

    def raised(self, token):
        return {'action': 'raise', 'player': token[0], 'action_chips': ast.literal_eval(token[1])}

    def bet(self, token):
        return {'action': 'raise', 'player': token[0], 'action_chips': ast.literal_eval(token[1])}

    def fold(self, token):
        return {'action': 'fold', 'player': token[0]}

    def call(self, token):
        return {'action': 'call', 'player': token[0], 'action_chips': ast.literal_eval(token[1])}

    def check(self, token):
        return {'action': 'check', 'player': token[0]}

    def timeout(self, token):
        return {'action': 'timeout', 'player': token[0]}

    def card(self, token):
        return {'value': token[0].value, 'suit': token[1].value}

    def check(self, token):
        return {'action': 'check', 'player': token[0]}

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
        return None

    def show_down_player(self, token):
        return None

    # def card_set(self, token):
        # return None

    # def total_pot(self, token):
    # # print(token[0])
    # # return ast.literal_eval(token[0])
    # return token[0]

    # def total_pot_many(self, token):
    # return ast.literal_eval(token[0])

    # def total_pot_single(self, token):
    # return ast.literal_eval(token[0])

    # def _street_actions(self, token, street):
    # act = 0
    # act_array = []
    # action_array = []
    # for i, v in enumerate(token):
    # action = v.children[0]
    # if isinstance(action, type(None)) or isinstance(action, Tree) or action['action'] == 'timeout':
    # continue
    # act_array.append(action['player'])
    # act = act_array.count(action['player'])
    # action_array.append(
    # {'player': action['player'], 'type': action['action'], 'id': i, 'act': act, 'position': ''})

    # # Position
    # positions = ['BB', 'SB', 'BTN', 'CO',
    #  'HJ', 'MP2', 'MP1', 'UTG+1', 'UTG']
    # i = 0
    # for a in reversed(action_array):
    # a['position'] = positions[i]

    # if i == 0:
    # first_a = a

    # if a['act'] != act:
    # if i == 2:
    # first_a['position'] = positions[2]
    # a['position'] = positions[0]
    # act = a['act']
    # i = 1
    # else:
    # i = i + 1

    # return action_array

    # Add Fact (just to add in order. Could be part of the prior FOR
    # for a in action_array:
    # self.engine.declare(Action(street=street, me=False, is_raised=False,
    #    player=a['player'], type=a['type'], id=a['id'], act=a['act'], position=a['position']))
