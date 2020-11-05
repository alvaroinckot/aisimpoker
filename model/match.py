class Match:
    def __init__(self):
        self.id = ''
        self.seats = []
        self.main_player = None
        self.initial_stack = None
        self.current_position = None

    def set_main_player(self, name):
        self.main_player = name
        try:
            seat = [player for player in self.seats if player['name'] == name]
            self.initial_stack = seat[0]['chips']
        except:
            # bug with lark interpreter
            print("Lark failed to parse hand. id: " + str(self.id))

    def get_decision_lines(self):
        if(self.main_player == None or self.initial_stack == None):
            # warning here :D
            return []
        return [{'id': self.id, 'player': self.main_player, 'initial_stack': self.initial_stack}]
