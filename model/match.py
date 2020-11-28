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
        self.hand_prime_product = 0
        self.tournament_progress = match_number
        self.same_suit = False
        self.pre_flop_actions = []
        self.flop_actions = []
        self.turn_actions = []
        self.river_actions = []
        self.pot = 0
        self.small_blind_player = None

    def set_hero(self, name):
        self.hero = name
        try:
            seat = [player for player in self.seats if player['name'] == name]
            self.initial_stack = seat[0]['chips']
            self.set_hero_position()
        except Exception as ex:
            print("Lark failed to parse hand. id: " + str(self.id))
            print(ex)

    def set_hand_card(self, cards):
        cardOne = Card.new(cards[0]['value'] + cards[0]['suit'])
        cardTwo = Card.new(cards[1]['value'] + cards[1]['suit'])
        self.same_suit = cards[0]['suit'] == cards[1]['suit']
        self.hand_prime_product = Card.prime_product_from_hand(
            [cardOne, cardTwo])
        self.hand_rank = evaluator.get_rank_class(self.hand_prime_product)

    def set_hero_position(self):
        positions = ['SB', 'BB', 'UTG', 'UTG+1',
                     'UTG+2', 'MP', 'MP2', 'CO', 'BTN']
        categories = {
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
        small_blind_index = next(
            (x for x in self.seats if x['name'] == self.small_blind_player), None)['seat'] - 1
        hero_index = next(
            (x for x in self.seats if x['name'] == self.hero), None)['seat'] - 1
        positions_rotated = positions[(small_blind_index * -1):] + \
            positions[:(small_blind_index * -1)]
        self.hero_position = positions_rotated[hero_index]
        self.hero_position_category = categories[self.hero_position]

    def add_pre_flop_action(self, action):
        hero_action = self.create_default_action('pre_flop', action)
        if(hero_action != None):
            hero_action['round'] = len(self.pre_flop_actions) + 1
            self.pre_flop_actions.append(hero_action)

    def add_flop_action(self, action):
        hero_action = self.create_default_action('flop', action)
        if(hero_action != None):
            hero_action['round'] = len(self.flop_actions) + 1
            self.flop_actions.append(hero_action)

    def add_turn_action(self, action):
        hero_action = self.create_default_action('turn', action)
        if(hero_action != None):
            hero_action['round'] = len(self.turn_actions) + 1
            self.turn_actions.append(hero_action)

    def add_river_action(self, action):
        hero_action = self.create_default_action('river', action)
        if(hero_action != None):
            hero_action['round'] = len(self.river_actions) + 1
            self.river_actions.append(hero_action)

    def create_default_action(self, street, action):
        sanitized_action = None

        if(action['player'] == self.hero and action['action'] != 'timeout'):
            sanitized_action = {
                # 'hero': self.hero,
                'action': action['action'],
                'street': street,
                'hand_initial_stack_bbs':  self.initial_stack / self.blind,
                'hand_rank': self.hand_rank,
                'same_suit': self.same_suit,
                'blind': self.blind,
                'tournament_progress': self.tournament_progress,
                'occupied_seats': len(self.seats),
                'pot_bbs': self.pot / self.blind,
                'position': self.hero_position,
                'position_category': self.hero_position_category
            }

        self.pot += action['action_chips']  # add all chips to the pot

        return sanitized_action
