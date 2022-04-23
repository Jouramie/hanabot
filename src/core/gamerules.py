from core.card import Suit

hand_size_rules = {2: 5, 3: 5, 4: 4, 5: 4, 6: 3}

suit_abbreviations = {
    Suit.RED: "Re",
    Suit.BLUE: "Bl",
    Suit.GREEN: "Gr",
    Suit.YELLOW: "Ye",
    Suit.PURPLE: "Pu",
    Suit.TEAL: "Te",
}


def get_hand_size(number_of_players: int) -> int:
    return hand_size_rules[number_of_players]


def get_suit_short_name(suit: Suit) -> str:
    return suit_abbreviations[suit]
