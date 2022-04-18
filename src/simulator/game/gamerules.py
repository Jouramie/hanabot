from core import Suit

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


def get_max_turns(number_players: int, number_suits: int) -> int:
    starting_clues = 8
    clues_per_discard = 1
    max_turns_per_deck_card = 1 + clues_per_discard
    total_cards = number_suits * 10
    hand_size = get_hand_size(number_players)
    cards_in_hands = hand_size * number_players
    deck_size = total_cards - cards_in_hands
    max_turns_from_emptying_deck = deck_size * max_turns_per_deck_card
    max_turns = max_turns_from_emptying_deck + number_players + starting_clues
    return max_turns


def get_suit_short_name(suit: Suit) -> str:
    return suit_abbreviations[suit]
