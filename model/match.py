class Match:
    def __init__(self):
        self.id = ''
        self.seats = []
        self.main_player = None
        self.initial_stack = None
        self.current_position = None
        self.actions = []

    def set_main_player(self, name):
        self.main_player = name
        try:
            seat = [player for player in self.seats if player['name'] == name]
            self.initial_stack = seat[0]['chips']
        except:
            print("Lark failed to parse hand. id: " + str(self.id))

    def add_player_action(self, street, action):
        if(action['player'] == self.main_player):
            action['street'] = street
            self.actions.append(action)
    # return [{'id': self.id, 'player': self.main_player, 'initial_stack': self.initial_stack}]
