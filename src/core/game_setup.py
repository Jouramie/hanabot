from frozendict import frozendict

player_names_per_player_number: dict[int, tuple[str, ...]] = frozendict(
    {
        2: ("Alice", "Bob"),
        3: ("Alice", "Bob", "Cathy"),
        4: ("Alice", "Bob", "Cathy", "Donald"),
        5: ("Alice", "Bob", "Cathy", "Donald", "Emily"),
        6: ("Alice", "Bob", "Cathy", "Donald", "Emily", "Frank"),
    }
)
