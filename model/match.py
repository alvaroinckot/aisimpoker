from treys import Card
from treys import Evaluator

evaluator = Evaluator()


class Match:
    def __init__(self, match_number):
        self.id = ''
        self.seats = []
        self.hero = None
        self.hero_position = None
        self.hero_position_category = None
        self.initial_stack = None
        self.current_position = None
        self.blind = 0
        self.hand_score = 0
        self.tournament_progress = match_number
        self.is_suited = False
        self.is_pair = False
        self.pre_flop_actions = []
        self.flop_actions = []
        self.turn_actions = []
        self.river_actions = []
        self.pot = 0
        self.small_blind_player = None
        self.hand_cards = []
        self.board_cards = []

        self.opponents_pre_flop_actions = []
        self.opponents_flop_actions = []
        self.opponents_turn_actions = []
        self.opponents_river_actions = []
        self.opponents_sitting_out = 0

        self.categories = {
            'SB': 'BLIND',
            'BB': 'BLIND',
            'UTG': 'EARLY',
            'UTG+1': 'EARLY',
            'UTG+2': 'EARLY',
            'MP': 'MIDDLE',
            'MP2': 'MIDDLE',
            'CO': 'LATE',
            'BTN': 'LATE',
        }

    def set_hero(self, name):
        self.hero = name
        try:
            seat = [player for player in self.seats if player['name'] == name]
            self.initial_stack = seat[0]['chips']
            self.set_hero_position()
        except Exception as ex:
            print("Lark failed to parse hand. id: " + str(self.id))
            print(ex)
            raise

    def set_hand_card(self, cards):
        self.hand_cards = cards
        cardOne = Card.new(cards[0]['value'] + cards[0]['suit'])
        cardTwo = Card.new(cards[1]['value'] + cards[1]['suit'])
        self.is_suited = cards[0]['suit'] == cards[1]['suit']
        self.is_pair = cards[0]['value'] == cards[1]['value']
        self.hand_score = Card.prime_product_from_hand(
            [cardOne, cardTwo])
        self.hand_rank = evaluator.get_rank_class(self.hand_score)

    def get_hand_with_board_rank_class(self):
        hand = [Card.new(card['value'] + card['suit'])
                for card in self.hand_cards]
        board = [Card.new(card['value'] + card['suit'])
                 for card in self.board_cards]
        score = evaluator.evaluate(board, hand)
        return evaluator.get_rank_class(score)

    def set_hero_position(self):
        positions = ['SB', 'BB', 'UTG', 'UTG+1',
                     'UTG+2', 'MP', 'MP2', 'CO', 'BTN']

        small_blind_index = next(
            (x for x in self.seats if x['name'] == self.small_blind_player), None)['seat'] - 1
        hero_index = next(
            (x for x in self.seats if x['name'] == self.hero), None)['seat'] - 1

        positions_rotated = positions[(small_blind_index * -1):] + \
            positions[:(small_blind_index * -1)]
        self.hero_position = positions_rotated[hero_index]
        self.hero_position_category = self.categories[self.hero_position]

    def set_board_cards(self, cards):
        self.board_cards = cards + self.board_cards

    def add_pre_flop_action(self, action):
        hero_action = self.create_default_action('pre_flop', action)
        if(hero_action != None):
            hero_action['round'] = len(self.pre_flop_actions) + 1
            hero_action['opponent_raise_count'] = len(
                [x for x in self.opponents_pre_flop_actions if x['action'] == 'raise'])
            hero_action['opponent_fold_count'] = len(
                [x for x in self.opponents_pre_flop_actions if x['action'] == 'fold'])
            hero_action['opponent_call_count'] = len(
                [x for x in self.opponents_pre_flop_actions if x['action'] == 'call'])
            self.pre_flop_actions.append(hero_action)
        else:
            self.opponents_pre_flop_actions.append(
                {
                    'action': action['action'],
                    'player': action['player'],
                }
            )

    def add_flop_action(self, action):
        hero_action = self.create_default_action('flop', action)
        if(hero_action != None):
            hero_action['round'] = len(self.flop_actions) + 1
            hero_action['hand_with_board_rank'] = self.get_hand_with_board_rank_class()
            hero_action['opponent_raise_count'] = len(
                [x for x in self.opponents_flop_actions if x['action'] == 'raise'])
            hero_action['opponent_fold_count'] = len(
                [x for x in self.opponents_flop_actions if x['action'] == 'fold'])
            hero_action['opponent_call_count'] = len(
                [x for x in self.opponents_flop_actions if x['action'] == 'call'])
            hero_action['opponent_check_count'] = len(
                [x for x in self.opponents_flop_actions if x['action'] == 'check'])
            self.flop_actions.append(hero_action)
        else:
            self.opponents_flop_actions.append(
                {
                    'action': action['action'],
                    'player': action['player'],
                }
            )

    def add_turn_action(self, action):
        hero_action = self.create_default_action('turn', action)
        if(hero_action != None):
            hero_action['round'] = len(self.turn_actions) + 1
            hero_action['hand_with_board_rank'] = self.get_hand_with_board_rank_class()
            hero_action['opponent_raise_count'] = len(
                [x for x in self.opponents_turn_actions if x['action'] == 'raise'])
            hero_action['opponent_fold_count'] = len(
                [x for x in self.opponents_turn_actions if x['action'] == 'fold'])
            hero_action['opponent_call_count'] = len(
                [x for x in self.opponents_turn_actions if x['action'] == 'call'])
            hero_action['opponent_check_count'] = len(
                [x for x in self.opponents_turn_actions if x['action'] == 'check'])
            self.turn_actions.append(hero_action)
        else:
            self.opponents_turn_actions.append(
                {
                    'action': action['action'],
                    'player': action['player'],
                }
            )

    def add_river_action(self, action):
        hero_action = self.create_default_action('river', action)
        if(hero_action != None):
            hero_action['round'] = len(self.river_actions) + 1
            hero_action['hand_with_board_rank'] = self.get_hand_with_board_rank_class()
            hero_action['opponent_raise_count'] = len(
                [x for x in self.opponents_river_actions if x['action'] == 'raise'])
            hero_action['opponent_fold_count'] = len(
                [x for x in self.opponents_river_actions if x['action'] == 'fold'])
            hero_action['opponent_call_count'] = len(
                [x for x in self.opponents_river_actions if x['action'] == 'call'])
            hero_action['opponent_check_count'] = len(
                [x for x in self.opponents_river_actions if x['action'] == 'check'])
            self.river_actions.append(hero_action)
        else:
            self.opponents_turn_actions.append(
                {
                    'action': action['action'],
                    'player': action['player'],
                }
            )

    def create_default_action(self, street, action):
        sanitized_action = None

        if(action['player'] == self.hero and action['action'] != 'timeout'):
            sanitized_action = {
                # 'hero': self.hero,
                'action': action['action'],
                'street': street,
                'hand_initial_stack_bbs':  "{:.2f}".format(self.initial_stack / self.blind),
                'hand_rank': self.hand_rank,
                'is_suited': self.is_suited,
                'is_pair': self.is_pair,
                'blind': self.blind,
                'tournament_progress': self.tournament_progress,
                'occupied_seats': len(self.seats),
                'pot_bbs': "{:.2f}".format(self.pot / self.blind),
                'position': self.hero_position,
                'position_category': self.hero_position_category,
                'total_players_bbs': "{:.2f}".format(sum([x['chips'] in x for x in self.seats])/self.blind),
                'opponents_sitting_out': self.opponents_sitting_out
            }

        self.pot += action['action_chips']  # add all chips to the pot

        return sanitized_action
