class Match:
    def __init__(self):
        self.id = ''
        self.seats = []
        self.main_player = None
        self.initial_stack = None
        self.current_position = None
        self.actions = []
        self.blind = 0

    def set_main_player(self, name):
        self.main_player = name
        try:
            seat = [player for player in self.seats if player['name'] == name]
            self.initial_stack = seat[0]['chips']
        except:
            print("Lark failed to parse hand. id: " + str(self.id))

    def add_player_action(self, street, action):
        if(action['player'] == self.main_player):
            if not 'action_chips' in action:
                action['action_chips'] = 0
                action['action_bbs'] = 0
            else:
                action['action_bbs'] = action['action_chips'] / self.blind
            action['street'] = street
            action['hand_initial_stack_chips'] = self.initial_stack
            action['hand_initial_stack_bbs'] = self.initial_stack / self.blind
            action['blind'] = self.blind
            self.actions.append(action)
