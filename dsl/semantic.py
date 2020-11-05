from lark import Lark, Transformer, v_args, Tree
import ast


class PokerSemantic(Transformer):

    def __init__(self, match):
        self.match = match
    # def hand(self, token):
    # self.engine.declare(Hand(id=int(token[0])))

    # def blind(self, token):
    # self.engine.declare(Blind(small=int(token[1]), big=int(token[2])))

    def player(self, token):
        # self.match.player = token[0].strip()
        self.match.players.append(token[0].strip())
        return token[0].strip()

    def received_card(self, token):
        self.match.main_player = token[1]

    def chips(self, token):
        return ast.literal_eval(token[0])

    def seat(self, token):
        return {'name': token[1], 'chips': token[2], 'seat': ast.literal_eval(token[0]),  'is_out': (len(token) == 4 and token[3].type == "IS_OUT")}

    def received_card(self, token):
        return {'player': token[0], 'cards': token[1].children}

        # def board(self, token):
        # self.engine.declare(Table(cards=token[0].children))

    def pre_flop(self, token):
        self._street_actions(token, 'PREFLOP')

    def flop(self, token):
        self._street_actions(token[2:], 'FLOP')

    def card(self, token):
        return {'value': token[0].value, 'suit': token[1].value}

    def fold(self, token):
        return {'action': 'fold', 'player': token[0]}

    def raised(self, token):
        return {'action': 'raise', 'player': token[0], 'chips': ast.literal_eval(token[1])}

    def call(self, token):
        return {'action': 'call', 'player': token[0], 'chips': ast.literal_eval(token[1])}

    def bet(self, token):
        return {'action': 'raise', 'player': token[0], 'chips': ast.literal_eval(token[1])}

    def check(self, token):
        return {'action': 'check', 'player': token[0]}

    def timeout(self, token):
        return {'action': 'timeout', 'player': token[0]}

    def chat(self, token):
        pass

    def uncalled_bet(self, token):
        pass

    def total_pot(self, token):
        print(token[0])
        # return ast.literal_eval(token[0])
        return token[0]

    def total_pot_many(self, token):
        return ast.literal_eval(token[0])

    def total_pot_single(self, token):
        return ast.literal_eval(token[0])

    def _street_actions(self, token, street):
        act = 0
        act_array = []
        action_array = []
        for i, v in enumerate(token):
            action = v.children[0]
            if isinstance(action, type(None)) or isinstance(action, Tree) or action['action'] == 'timeout':
                continue
            act_array.append(action['player'])
            act = act_array.count(action['player'])
            action_array.append(
                {'player': action['player'], 'type': action['action'], 'id': i, 'act': act, 'position': ''})

        # Position
        positions = ['BB', 'SB', 'BTN', 'CO',
                     'HJ', 'MP2', 'MP1', 'UTG+1', 'UTG']
        i = 0
        for a in reversed(action_array):
            a['position'] = positions[i]

            if i == 0:
                first_a = a

            if a['act'] != act:
                if i == 2:
                    first_a['position'] = positions[2]
                a['position'] = positions[0]
                act = a['act']
                i = 1
            else:
                i = i + 1

        # Add Fact (just to add in order. Could be part of the prior FOR
        # for a in action_array:
            # self.engine.declare(Action(street=street, me=False, is_raised=False,
                #    player=a['player'], type=a['type'], id=a['id'], act=a['act'], position=a['position']))
