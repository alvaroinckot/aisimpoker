from treys import Card
from treys import Evaluator

evaluator = Evaluator()


class Match:
    def __init__(self, match_number):
        self.id = ''
        self.seats = []
        self.hero = None
        self.initial_stack = None
        self.current_position = None
        self.actions = []
        self.blind = 0
        self.hand_prime_product = 0
        self.tournament_progress = match_number

    def set_hero(self, name):
        self.hero = name
        try:
            seat = [player for player in self.seats if player['name'] == name]
            self.initial_stack = seat[0]['chips']
        except:
            print("Lark failed to parse hand. id: " + str(self.id))

    def set_hand_card(self, cards):
        cardOne = Card.new(cards[0]['value'] + cards[0]['suit'])
        cardTwo = Card.new(cards[1]['value'] + cards[1]['suit'])
        self.hand_prime_product = Card.prime_product_from_hand(
            [cardOne, cardTwo])
        self.hand_rank = evaluator.get_rank_class(self.hand_prime_product)

    def add_player_action(self, street, action):
        if(action['player'] == self.hero and action['action'] != 'timeout'):
            sanitized_action = {
                'hero': self.hero,
                'action': action['action'],
                'street': street,
                'hand_initial_stack_bbs':  self.initial_stack / self.blind,
                'hand_prime_product': self.hand_prime_product,
                'hand_rank': self.hand_rank,
                'blind': self.blind,
                'tournament_progress': self.tournament_progress
            }
            self.actions.append(sanitized_action)
