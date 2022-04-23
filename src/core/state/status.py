class Status:
    current_turn: int
    current_clues: int
    current_strikes: int
    is_over: bool
    turns_remaining: int

    def __init__(self):
        self.current_turn = 0
        self.current_clues = 8
        self.current_strikes = 0
        self.is_over = False
