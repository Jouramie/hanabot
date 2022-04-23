class Status:
    turn: int
    clues: int
    strikes: int
    is_over: bool
    turns_remaining: int

    def __init__(self):
        self.turn = 0
        self.clues = 8
        self.strikes = 0
        self.is_over = False

    def generate_clue(self):
        self.clues = self.clues + 1

    def consume_clue(self):
        if self.clues < 1:
            raise ValueError("You cannot give a clue, the team has no clues!")
        self.clues = self.clues - 1

    def add_strike(self):
        self.strikes = self.strikes + 1
        if self.strikes >= 3:
            self.is_over = True

    def next_turn(self):
        self.turn = self.turn + 1
