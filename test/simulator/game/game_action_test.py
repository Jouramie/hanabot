import pytest

from core import Deck, Card, Suit, Rank
from core.state.gamestate import GameState
from simulator.game.action import ColorClueAction, RankClueAction, PlayAction, DiscardAction
from simulator.game.clue import ColorClue, RankClue
from simulator.game.game import Game
from test.simulator.game.game_setup import get_player_names, get_ranks


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_give_color_clue_should_use_clue(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    second_player = game.players[1]
    second_card = second_player.hand[1].real_card
    action = ColorClueAction(second_card.suit, second_player)

    clues_before_action = game.status.clues
    game.play_turn(action)
    clues_after_action = game.status.clues
    assert clues_before_action == clues_after_action + 1


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_give_rank_clue_should_use_clue(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    second_player = game.players[1]
    second_card = second_player.hand[1].real_card
    action = RankClueAction(second_card.rank, second_player)

    clues_before_action = game.status.clues
    game.play_turn(action)
    clues_after_action = game.status.clues
    assert clues_before_action == clues_after_action + 1


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_give_color_clue_should_add_clue_on_all_hand_cards(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    first_player = game.players[0]
    second_player = game.players[1]
    second_card = second_player.hand[1].real_card

    for hand_card in second_player.hand:
        assert len(hand_card.received_clues) == 0

    action = ColorClueAction(second_card.suit, second_player)
    game.play_turn(action)

    for slot, hand_card in enumerate(second_player.hand):
        assert len(hand_card.received_clues) == 1
        received_clue = hand_card.received_clues[0]
        assert not hand_card.is_clued or slot in received_clue.touched_slots
        assert received_clue.turn == 1
        assert received_clue.giver_name == first_player.name
        assert received_clue.receiver_name == second_player.name
        assert isinstance(received_clue, ColorClue)
        assert received_clue.suit == second_card.suit


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_give_rank_clue_should_add_clue_on_all_hand_cards(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    first_player = game.players[0]
    second_player = game.players[1]
    second_card = second_player.hand[1].real_card

    for hand_card in second_player.hand:
        assert len(hand_card.received_clues) == 0

    action = RankClueAction(second_card.rank, second_player)
    game.play_turn(action)

    for slot, hand_card in enumerate(second_player.hand):
        assert len(hand_card.received_clues) == 1
        received_clue = hand_card.received_clues[0]
        assert not hand_card.is_clued or slot in received_clue.touched_slots
        assert received_clue.turn == 1
        assert received_clue.giver_name == first_player.name
        assert received_clue.receiver_name == second_player.name
        assert isinstance(received_clue, RankClue)
        assert received_clue.rank == second_card.rank


@pytest.mark.parametrize("number_players", [number_players for number_players in range(3, 7)])
def test_give_two_clues_should_add_clues_on_all_hand_cards(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    first_player = game.players[0]
    second_player = game.players[1]
    third_player = game.players[2]
    second_card = third_player.hand[1].real_card

    for hand_card in third_player.hand:
        assert len(hand_card.received_clues) == 0

    action1 = ColorClueAction(second_card.suit, third_player)
    action2 = RankClueAction(second_card.rank, third_player)
    game.play_turn(action1)
    game.play_turn(action2)

    for hand_card in third_player.hand:
        assert len(hand_card.received_clues) == 2
        first_received_clue = hand_card.received_clues[0]
        second_received_clue = hand_card.received_clues[1]

        assert first_received_clue.turn == 1
        assert first_received_clue.giver_name == first_player.name
        assert first_received_clue.receiver_name == third_player.name
        assert isinstance(first_received_clue, ColorClue)
        assert first_received_clue.suit == second_card.suit

        assert second_received_clue.turn == 2
        assert second_received_clue.giver_name == second_player.name
        assert second_received_clue.receiver_name == third_player.name
        assert isinstance(second_received_clue, RankClue)
        assert second_received_clue.rank == second_card.rank


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_give_color_clue_should_add_clue_to_history(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    first_player = game.players[0]
    second_player = game.players[1]
    second_card = second_player.hand[1].real_card

    assert len(game.history.clues) == 0

    action = ColorClueAction(second_card.suit, second_player)
    game.play_turn(action)

    assert len(game.history.clues) == 1
    history_clue = game.history.clues[0]
    assert history_clue.turn == 1
    assert history_clue.giver_name == first_player.name
    assert history_clue.receiver_name == second_player.name
    assert isinstance(history_clue, ColorClue)
    assert history_clue.suit == second_card.suit


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_give_rank_clue_should_add_clue_to_history(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    first_player = game.players[0]
    second_player = game.players[1]
    second_card = second_player.hand[1].real_card

    assert len(game.history.clues) == 0

    action = RankClueAction(second_card.rank, second_player)
    game.play_turn(action)

    assert len(game.history.clues) == 1
    history_clue = game.history.clues[0]
    assert history_clue.turn == 1
    assert history_clue.giver_name == first_player.name
    assert history_clue.receiver_name == second_player.name
    assert isinstance(history_clue, RankClue)
    assert history_clue.rank == second_card.rank


@pytest.mark.parametrize("number_players", [number_players for number_players in range(3, 7)])
def test_give_two_clues_should_add_both_clues_to_history(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    first_player = game.players[0]
    second_player = game.players[1]
    third_player = game.players[2]
    second_card = third_player.hand[1].real_card

    assert len(game.history.clues) == 0

    action1 = ColorClueAction(second_card.suit, third_player)
    action2 = RankClueAction(second_card.rank, third_player)
    game.play_turn(action1)
    assert len(game.history.clues) == 1
    game.play_turn(action2)

    assert len(game.history.clues) == 2

    history_clue1 = game.history.clues[0]
    assert history_clue1.turn == 1
    assert history_clue1.giver_name == first_player.name
    assert history_clue1.receiver_name == third_player.name
    assert isinstance(history_clue1, ColorClue)
    assert history_clue1.suit == second_card.suit

    history_clue2 = game.history.clues[1]
    assert history_clue2.turn == 2
    assert history_clue2.giver_name == second_player.name
    assert history_clue2.receiver_name == third_player.name
    assert isinstance(history_clue2, RankClue)
    assert history_clue2.rank == second_card.rank


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_play_should_draw_card(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    player = game.players[game.player_turn]

    slot0_before = player.hand[0]
    slot1_before = player.hand[1]
    slot2_before = player.hand[2]

    action = PlayAction(1)
    game.play_turn(action)

    slot0_after = player.hand[0]
    slot1_after = player.hand[1]
    slot2_after = player.hand[2]

    assert slot0_before != slot0_after
    assert slot0_before == slot1_after
    assert slot2_before == slot2_after


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_discard_should_draw_card(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    player = game.players[game.player_turn]
    game.status.clues = 4

    slot0_before = player.hand[0]
    slot1_before = player.hand[1]
    slot2_before = player.hand[2]

    action = DiscardAction(1)
    game.play_turn(action)

    slot0_after = player.hand[0]
    slot1_after = player.hand[1]
    slot2_after = player.hand[2]

    assert slot0_before != slot0_after
    assert slot0_before == slot1_after
    assert slot2_before == slot2_after


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_color_clue_should_not_draw_card(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    player = game.players[game.player_turn]

    slot0_before = player.hand[0]
    slot1_before = player.hand[1]
    slot2_before = player.hand[2]

    second_player = game.players[1]
    second_card = second_player.hand[1].real_card
    action = ColorClueAction(second_card.suit, second_player)
    game.play_turn(action)

    slot0_after = player.hand[0]
    slot1_after = player.hand[1]
    slot2_after = player.hand[2]

    assert slot0_before == slot0_after
    assert slot1_before == slot1_after
    assert slot2_before == slot2_after


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_rank_clue_should_not_draw_card(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    player = game.players[game.player_turn]

    slot0_before = player.hand[0]
    slot1_before = player.hand[1]
    slot2_before = player.hand[2]

    second_player = game.players[1]
    second_card = second_player.hand[1].real_card
    action = RankClueAction(second_card.rank, second_player)
    game.play_turn(action)

    slot0_after = player.hand[0]
    slot1_after = player.hand[1]
    slot2_after = player.hand[2]

    assert slot0_before == slot0_after
    assert slot1_before == slot1_after
    assert slot2_before == slot2_after


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_empty_deck_play_should_not_draw_card(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    player = game.players[game.player_turn]
    game.current_state.deck = Deck.empty()

    slot0_before = player.hand[0]
    slot1_before = player.hand[1]
    slot2_before = player.hand[2]

    action = PlayAction(1)
    game.play_turn(action)

    slot0_after = player.hand[0]
    slot1_after = player.hand[1]

    assert slot0_before == slot0_after
    assert slot2_before == slot1_after


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_empty_deck_discard_should_not_draw_card(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    player = game.players[game.player_turn]
    game.status.clues = 4
    game.current_state.deck = Deck.empty()

    slot0_before = player.hand[0]
    slot1_before = player.hand[1]
    slot2_before = player.hand[2]

    action = DiscardAction(1)
    game.play_turn(action)

    slot0_after = player.hand[0]
    slot1_after = player.hand[1]

    assert slot0_before == slot0_after
    assert slot2_before == slot1_after


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_empty_deck_color_clue_should_not_draw_card(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    player = game.players[game.player_turn]
    game.current_state.deck = Deck.empty()

    slot0_before = player.hand[0]
    slot1_before = player.hand[1]
    slot2_before = player.hand[2]

    second_player = game.players[1]
    second_card = second_player.hand[1].real_card
    action = ColorClueAction(second_card.suit, second_player)
    game.play_turn(action)

    slot0_after = player.hand[0]
    slot1_after = player.hand[1]
    slot2_after = player.hand[2]

    assert slot0_before == slot0_after
    assert slot1_before == slot1_after
    assert slot2_before == slot2_after


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_empty_deck_rank_clue_should_not_draw_card(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    player = game.players[game.player_turn]
    game.current_state.deck = Deck.empty()

    slot0_before = player.hand[0]
    slot1_before = player.hand[1]
    slot2_before = player.hand[2]

    second_player = game.players[1]
    second_card = second_player.hand[1].real_card
    action = RankClueAction(second_card.rank, second_player)
    game.play_turn(action)

    slot0_after = player.hand[0]
    slot1_after = player.hand[1]
    slot2_after = player.hand[2]

    assert slot0_before == slot0_after
    assert slot1_before == slot1_after
    assert slot2_before == slot2_after


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_discard_should_add_card_to_discard_pile(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    player = game.players[game.player_turn]
    game.status.clues = 4

    slot2_before = player.hand[2].real_card

    assert game.current_state.count_discarded(slot2_before) == 0

    action = DiscardAction(2)
    game.play_turn(action)

    assert game.current_state.count_discarded(slot2_before) == 1


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_play_fail_should_add_card_to_discard_pile(number_players):
    game = Game(get_player_names(number_players), Deck.starting_with(Card(Suit.RED, Rank.FOUR)))
    player = game.players[game.player_turn]

    last_slot_before = player.hand[-1].real_card

    assert game.current_state.count_discarded(last_slot_before) == 0

    action = PlayAction(len(player.hand) - 1)
    game.play_turn(action)

    assert game.current_state.count_discarded(last_slot_before) == 1


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_play_fail_should_add_strike(number_players):
    game = Game(get_player_names(number_players), Deck.starting_with(Card(Suit.RED, Rank.FOUR)))
    player = game.players[game.player_turn]

    strikes_before = game.status.strikes

    action = PlayAction(len(player.hand) - 1)
    game.play_turn(action)

    strikes_after = game.status.strikes
    assert strikes_after == strikes_before + 1


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_color_cluing_with_a_deck_should_not_reduce_number_of_turns_remaining(number_players):
    game = Game(get_player_names(number_players), Deck.generate())

    turns_remaining_before = game.status.turns_remaining

    second_player = game.players[1]
    second_card = second_player.hand[1].real_card
    action = ColorClueAction(second_card.suit, second_player)
    game.play_turn(action)

    turns_remaining_after = game.status.turns_remaining

    assert turns_remaining_before == turns_remaining_after


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_rank_cluing_with_a_deck_should_not_reduce_number_of_turns_remaining(number_players):
    game = Game(get_player_names(number_players), Deck.generate())

    turns_remaining_before = game.status.turns_remaining

    second_player = game.players[1]
    second_card = second_player.hand[1].real_card
    action = RankClueAction(second_card.rank, second_player)
    game.play_turn(action)

    turns_remaining_after = game.status.turns_remaining

    assert turns_remaining_before == turns_remaining_after


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_color_cluing_empty_deck_should_reduce_number_of_turns_remaining(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    game.current_state.deck = Deck.empty()

    turns_remaining_before = game.status.turns_remaining

    second_player = game.players[1]
    second_card = second_player.hand[1].real_card
    action = ColorClueAction(second_card.suit, second_player)
    game.play_turn(action)

    turns_remaining_after = game.status.turns_remaining

    assert turns_remaining_before == turns_remaining_after + 1


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_rank_cluing_empty_deck_should_reduce_number_of_turns_remaining(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    game.current_state.deck = Deck.empty()

    turns_remaining_before = game.status.turns_remaining

    second_player = game.players[1]
    second_card = second_player.hand[1].real_card
    action = RankClueAction(second_card.rank, second_player)
    game.play_turn(action)

    turns_remaining_after = game.status.turns_remaining

    assert turns_remaining_before == turns_remaining_after + 1


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_playing_successfully_with_a_deck_should_reduce_number_of_turns_remaining(number_players):
    game = Game(get_player_names(number_players), Deck.starting_with(Card(Suit.RED, Rank.ONE)))

    turns_remaining_before = game.status.turns_remaining
    action = PlayAction(len(game.players[0].hand) - 1)
    game.play_turn(action)

    turns_remaining_after = game.status.turns_remaining

    assert turns_remaining_before == turns_remaining_after + 1


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_playing_successfully_without_a_deck_should_reduce_number_of_turns_remaining(number_players):
    game = Game(get_player_names(number_players), Deck.starting_with(Card(Suit.RED, Rank.ONE)))
    game.current_state.deck = Deck.empty()

    turns_remaining_before = game.status.turns_remaining
    action = PlayAction(len(game.players[0].hand) - 1)
    game.play_turn(action)

    turns_remaining_after = game.status.turns_remaining

    assert turns_remaining_before == turns_remaining_after + 1


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_playing_failed_with_a_deck_should_reduce_number_of_turns_remaining(number_players):
    game = Game(get_player_names(number_players), Deck.starting_with(Card(Suit.RED, Rank.FOUR)))

    turns_remaining_before = game.status.turns_remaining
    action = PlayAction(len(game.players[0].hand) - 1)
    game.play_turn(action)

    turns_remaining_after = game.status.turns_remaining

    assert turns_remaining_before == turns_remaining_after + 1


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_playing_failed_without_a_deck_should_reduce_number_of_turns_remaining(number_players):
    game = Game(get_player_names(number_players), Deck.starting_with(Card(Suit.RED, Rank.FOUR)))
    game.current_state.deck = Deck.empty()

    turns_remaining_before = game.status.turns_remaining
    action = PlayAction(len(game.players[0].hand) - 1)
    game.play_turn(action)

    turns_remaining_after = game.status.turns_remaining

    assert turns_remaining_before == turns_remaining_after + 1


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_discard_with_a_deck_should_reduce_number_of_turns_remaining(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    game.status.clues = 4

    turns_remaining_before = game.status.turns_remaining
    action = DiscardAction(0)
    game.play_turn(action)

    turns_remaining_after = game.status.turns_remaining

    assert turns_remaining_before == turns_remaining_after + 1


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_discard_without_a_deck_should_reduce_number_of_turns_remaining(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    game.current_state.deck = Deck.empty()
    game.status.clues = 4

    turns_remaining_before = game.status.turns_remaining
    action = DiscardAction(0)
    game.play_turn(action)

    turns_remaining_after = game.status.turns_remaining

    assert turns_remaining_before == turns_remaining_after + 1


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_discard_should_add_state_to_history(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    game.status.clues = 4

    action = DiscardAction(0)
    game.play_turn(action)

    turn_0_state = game.history.get_state_at_turn(0)
    assert isinstance(turn_0_state, GameState)
    assert turn_0_state.status.clues == 4
    assert game.current_state.status.clues == 5


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_playing_failed_should_add_state_to_history(number_players):
    game = Game(get_player_names(number_players), Deck.starting_with(Card(Suit.RED, Rank.FOUR)))

    action = PlayAction(len(game.players[0].hand) - 1)
    game.play_turn(action)

    turn_0_state = game.history.get_state_at_turn(0)
    assert isinstance(turn_0_state, GameState)
    assert turn_0_state.status.strikes == 0
    assert game.current_state.status.strikes == 1


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_playing_success_should_add_state_to_history(number_players):
    game = Game(get_player_names(number_players), Deck.starting_with(Card(Suit.RED, Rank.ONE)))

    action = PlayAction(len(game.players[0].hand) - 1)
    game.play_turn(action)

    turn_0_state = game.history.get_state_at_turn(0)
    assert isinstance(turn_0_state, GameState)
    assert turn_0_state.status.turns_remaining == game.current_state.status.turns_remaining + 1


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_color_clue_should_add_state_to_history(number_players):
    game = Game(get_player_names(number_players), Deck.generate())

    second_player = game.players[1]
    second_card = second_player.hand[1].real_card
    action = ColorClueAction(second_card.suit, second_player)
    game.play_turn(action)

    turn_0_state = game.history.get_state_at_turn(0)
    assert isinstance(turn_0_state, GameState)
    assert turn_0_state.status.clues == 8
    assert game.current_state.status.clues == 7


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_color_clue_should_add_state_to_history(number_players):
    game = Game(get_player_names(number_players), Deck.generate())

    second_player = game.players[1]
    second_card = second_player.hand[1].real_card
    action = RankClueAction(second_card.rank, second_player)
    game.play_turn(action)

    turn_0_state = game.history.get_state_at_turn(0)
    assert isinstance(turn_0_state, GameState)
    assert turn_0_state.status.clues == 8
    assert game.current_state.status.clues == 7


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_discard_should_generate_clue(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    player = game.players[game.player_turn]
    game.status.clues = 4
    clues_before = game.status.clues

    action = DiscardAction(2)
    game.play_turn(action)

    clues_after = game.status.clues
    assert clues_after == clues_before + 1


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
@pytest.mark.parametrize("rank", [rank for rank in [Rank.ONE, Rank.TWO, Rank.THREE, Rank.FOUR]])
def test_play_should_not_generate_clue(number_players, rank):
    game = Game(get_player_names(number_players), Deck.starting_with(Card(Suit.RED, rank)))
    player = game.players[game.player_turn]
    for played_rank in get_ranks():
        if played_rank == rank:
            break
        game.current_state, _ = game.current_state.play(Card(Suit.RED, played_rank))
    game.status.clues = 4
    clues_before = game.status.clues

    action = PlayAction(len(game.players[0].hand) - 1)
    game.play_turn(action)

    clues_after = game.status.clues
    assert clues_after == clues_before


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_play_five_should_generate_clue(number_players):
    game = Game(get_player_names(number_players), Deck.starting_with(Card(Suit.RED, Rank.FIVE)))
    player = game.players[game.player_turn]
    for played_rank in get_ranks():
        if played_rank == Rank.FIVE:
            break
        game.current_state, _ = game.current_state.play(Card(Suit.RED, played_rank))
    game.status.clues = 4
    clues_before = game.status.clues

    action = PlayAction(len(game.players[0].hand) - 1)
    game.play_turn(action)

    clues_after = game.status.clues
    assert clues_after == clues_before + 1
