class Status:
    turn: int
    clues: int
    strikes: int
    is_over: bool
    turns_remaining: int

    def __init__(self, turns_remaining: int):
        self.turn = 0
        self.clues = 8
        self.strikes = 0
        self.is_over = False
        self.turns_remaining = turns_remaining

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

    def decrement_turns_remaining(self):
        self.turns_remaining -= 1
        if self.turns_remaining <= 0:
            self.is_over = True
