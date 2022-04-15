hand_size_rules = {
    2: 5,
    3: 5,
    4: 4,
    5: 4,
    6: 3
}


def get_hand_size(number_of_players: int) -> int:
    return hand_size_rules[number_of_players]

