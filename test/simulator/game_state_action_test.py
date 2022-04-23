from simulator.game.action import ColorClueAction, RankClueAction, PlayAction, DiscardAction
from simulator.game.clue import ColorClue, RankClue
from test.simulator.game_setup import get_player_names, get_suits

from simulator.game.gamestate import GameState


def test_give_color_clue_should_use_clue():
    gamestate = GameState(get_player_names(5), get_suits(5))
    second_player = gamestate.players[1]
    second_card = second_player.hand[1].real_card
    action = ColorClueAction(second_card.suit, second_player)

    clues_before_action = gamestate.current_clues
    gamestate.play_turn(action)
    clues_after_action = gamestate.current_clues
    assert clues_before_action == clues_after_action + 1


def test_give_rank_clue_should_use_clue():
    gamestate = GameState(get_player_names(5), get_suits(5))
    second_player = gamestate.players[1]
    second_card = second_player.hand[1].real_card
    action = RankClueAction(second_card.rank, second_player)

    clues_before_action = gamestate.current_clues
    gamestate.play_turn(action)
    clues_after_action = gamestate.current_clues
    assert clues_before_action == clues_after_action + 1


def test_give_color_clue_should_add_clue_on_all_hand_cards():
    gamestate = GameState(get_player_names(5), get_suits(5))
    first_player = gamestate.players[0]
    second_player = gamestate.players[1]
    second_card = second_player.hand[1].real_card

    for hand_card in second_player.hand:
        assert len(hand_card.received_clues) == 0

    action = ColorClueAction(second_card.suit, second_player)
    gamestate.play_turn(action)

    for hand_card in second_player.hand:
        assert len(hand_card.received_clues) == 1
        received_clue = hand_card.received_clues[0]
        assert received_clue.turn == 1
        assert received_clue.giver_name == first_player.name
        assert received_clue.receiver_name == second_player.name
        assert isinstance(received_clue, ColorClue)
        assert received_clue.suit == second_card.suit


def test_give_rank_clue_should_add_clue_on_all_hand_cards():
    gamestate = GameState(get_player_names(5), get_suits(5))
    first_player = gamestate.players[0]
    second_player = gamestate.players[1]
    second_card = second_player.hand[1].real_card

    for hand_card in second_player.hand:
        assert len(hand_card.received_clues) == 0

    action = RankClueAction(second_card.rank, second_player)
    gamestate.play_turn(action)

    for hand_card in second_player.hand:
        assert len(hand_card.received_clues) == 1
        received_clue = hand_card.received_clues[0]
        assert received_clue.turn == 1
        assert received_clue.giver_name == first_player.name
        assert received_clue.receiver_name == second_player.name
        assert isinstance(received_clue, RankClue)
        assert received_clue.rank == second_card.rank


def test_give_two_clues_should_add_clues_on_all_hand_cards():
    gamestate = GameState(get_player_names(5), get_suits(5))
    first_player = gamestate.players[0]
    second_player = gamestate.players[1]
    third_player = gamestate.players[2]
    second_card = third_player.hand[1].real_card

    for hand_card in third_player.hand:
        assert len(hand_card.received_clues) == 0

    action1 = ColorClueAction(second_card.suit, third_player)
    action2 = RankClueAction(second_card.rank, third_player)
    gamestate.play_turn(action1)
    gamestate.play_turn(action2)

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


def test_give_color_clue_should_add_clue_to_history():
    gamestate = GameState(get_player_names(5), get_suits(5))
    first_player = gamestate.players[0]
    second_player = gamestate.players[1]
    second_card = second_player.hand[1].real_card

    assert len(gamestate.clue_history) == 0

    action = ColorClueAction(second_card.suit, second_player)
    gamestate.play_turn(action)

    assert len(gamestate.clue_history) == 1
    history_clue = gamestate.clue_history[0]
    assert history_clue.turn == 1
    assert history_clue.giver_name == first_player.name
    assert history_clue.receiver_name == second_player.name
    assert isinstance(history_clue, ColorClue)
    assert history_clue.suit == second_card.suit


def test_give_rank_clue_should_add_clue_to_history():
    gamestate = GameState(get_player_names(5), get_suits(5))
    first_player = gamestate.players[0]
    second_player = gamestate.players[1]
    second_card = second_player.hand[1].real_card

    assert len(gamestate.clue_history) == 0

    action = RankClueAction(second_card.rank, second_player)
    gamestate.play_turn(action)

    assert len(gamestate.clue_history) == 1
    history_clue = gamestate.clue_history[0]
    assert history_clue.turn == 1
    assert history_clue.giver_name == first_player.name
    assert history_clue.receiver_name == second_player.name
    assert isinstance(history_clue, RankClue)
    assert history_clue.rank == second_card.rank


def test_give_two_clues_should_add_both_clues_to_history():
    gamestate = GameState(get_player_names(5), get_suits(5))
    first_player = gamestate.players[0]
    second_player = gamestate.players[1]
    third_player = gamestate.players[2]
    second_card = third_player.hand[1].real_card

    assert len(gamestate.clue_history) == 0

    action1 = ColorClueAction(second_card.suit, third_player)
    action2 = RankClueAction(second_card.rank, third_player)
    gamestate.play_turn(action1)
    assert len(gamestate.clue_history) == 1
    gamestate.play_turn(action2)

    assert len(gamestate.clue_history) == 2

    history_clue1 = gamestate.clue_history[0]
    assert history_clue1.turn == 1
    assert history_clue1.giver_name == first_player.name
    assert history_clue1.receiver_name == third_player.name
    assert isinstance(history_clue1, ColorClue)
    assert history_clue1.suit == second_card.suit

    history_clue2 = gamestate.clue_history[1]
    assert history_clue2.turn == 2
    assert history_clue2.giver_name == second_player.name
    assert history_clue2.receiver_name == third_player.name
    assert isinstance(history_clue2, RankClue)
    assert history_clue2.rank == second_card.rank


def test_play_should_draw_card():
    gamestate = GameState(get_player_names(5), get_suits(5))
    player = gamestate.players[gamestate.player_turn]

    slot0_before = player.hand[0]
    slot1_before = player.hand[1]
    slot2_before = player.hand[2]
    slot3_before = player.hand[3]

    action = PlayAction(2)
    gamestate.play_turn(action)

    slot0_after = player.hand[0]
    slot1_after = player.hand[1]
    slot2_after = player.hand[2]
    slot3_after = player.hand[3]

    assert slot0_before != slot0_after
    assert slot0_before == slot1_after
    assert slot1_before == slot2_after
    assert slot2_before != slot2_after
    assert slot3_before == slot3_after


def test_discard_should_draw_card():
    gamestate = GameState(get_player_names(5), get_suits(5))
    player = gamestate.players[gamestate.player_turn]
    gamestate.current_clues = 4

    slot0_before = player.hand[0]
    slot1_before = player.hand[1]
    slot2_before = player.hand[2]
    slot3_before = player.hand[3]

    action = DiscardAction(2)
    gamestate.play_turn(action)

    slot0_after = player.hand[0]
    slot1_after = player.hand[1]
    slot2_after = player.hand[2]
    slot3_after = player.hand[3]

    assert slot0_before != slot0_after
    assert slot0_before == slot1_after
    assert slot1_before == slot2_after
    assert slot2_before != slot2_after
    assert slot3_before == slot3_after


def test_color_clue_should_not_draw_card():
    gamestate = GameState(get_player_names(5), get_suits(5))
    player = gamestate.players[gamestate.player_turn]

    slot0_before = player.hand[0]
    slot1_before = player.hand[1]
    slot2_before = player.hand[2]
    slot3_before = player.hand[3]

    second_player = gamestate.players[1]
    second_card = second_player.hand[1].real_card
    action = ColorClueAction(second_card.suit, second_player)
    gamestate.play_turn(action)

    slot0_after = player.hand[0]
    slot1_after = player.hand[1]
    slot2_after = player.hand[2]
    slot3_after = player.hand[3]

    assert slot0_before == slot0_after
    assert slot1_before == slot1_after
    assert slot2_before == slot2_after
    assert slot3_before == slot3_after


def test_rank_clue_should_not_draw_card():
    gamestate = GameState(get_player_names(5), get_suits(5))
    player = gamestate.players[gamestate.player_turn]

    slot0_before = player.hand[0]
    slot1_before = player.hand[1]
    slot2_before = player.hand[2]
    slot3_before = player.hand[3]

    second_player = gamestate.players[1]
    second_card = second_player.hand[1].real_card
    action = RankClueAction(second_card.rank, second_player)
    gamestate.play_turn(action)

    slot0_after = player.hand[0]
    slot1_after = player.hand[1]
    slot2_after = player.hand[2]
    slot3_after = player.hand[3]

    assert slot0_before == slot0_after
    assert slot1_before == slot1_after
    assert slot2_before == slot2_after
    assert slot3_before == slot3_after


def test_empty_deck_play_should_not_draw_card():
    gamestate = GameState(get_player_names(5), get_suits(5))
    player = gamestate.players[gamestate.player_turn]
    gamestate.deck = []

    slot0_before = player.hand[0]
    slot1_before = player.hand[1]
    slot2_before = player.hand[2]
    slot3_before = player.hand[3]

    action = PlayAction(2)
    gamestate.play_turn(action)

    slot0_after = player.hand[0]
    slot1_after = player.hand[1]
    slot2_after = player.hand[2]

    assert slot0_before == slot0_after
    assert slot1_before == slot1_after
    assert slot3_before == slot2_after


def test_empty_deck_discard_should_not_draw_card():
    gamestate = GameState(get_player_names(5), get_suits(5))
    player = gamestate.players[gamestate.player_turn]
    gamestate.current_clues = 4
    gamestate.deck = []

    slot0_before = player.hand[0]
    slot1_before = player.hand[1]
    slot2_before = player.hand[2]
    slot3_before = player.hand[3]

    action = DiscardAction(2)
    gamestate.play_turn(action)

    slot0_after = player.hand[0]
    slot1_after = player.hand[1]
    slot2_after = player.hand[2]

    assert slot0_before == slot0_after
    assert slot1_before == slot1_after
    assert slot3_before == slot2_after


def test_empty_deck_color_clue_should_not_draw_card():
    gamestate = GameState(get_player_names(5), get_suits(5))
    player = gamestate.players[gamestate.player_turn]
    gamestate.deck = []

    slot0_before = player.hand[0]
    slot1_before = player.hand[1]
    slot2_before = player.hand[2]
    slot3_before = player.hand[3]

    second_player = gamestate.players[1]
    second_card = second_player.hand[1].real_card
    action = ColorClueAction(second_card.suit, second_player)
    gamestate.play_turn(action)

    slot0_after = player.hand[0]
    slot1_after = player.hand[1]
    slot2_after = player.hand[2]
    slot3_after = player.hand[3]

    assert slot0_before == slot0_after
    assert slot1_before == slot1_after
    assert slot2_before == slot2_after
    assert slot3_before == slot3_after


def test_empty_deck_rank_clue_should_not_draw_card():
    gamestate = GameState(get_player_names(5), get_suits(5))
    player = gamestate.players[gamestate.player_turn]
    gamestate.deck = []

    slot0_before = player.hand[0]
    slot1_before = player.hand[1]
    slot2_before = player.hand[2]
    slot3_before = player.hand[3]

    second_player = gamestate.players[1]
    second_card = second_player.hand[1].real_card
    action = RankClueAction(second_card.rank, second_player)
    gamestate.play_turn(action)

    slot0_after = player.hand[0]
    slot1_after = player.hand[1]
    slot2_after = player.hand[2]
    slot3_after = player.hand[3]

    assert slot0_before == slot0_after
    assert slot1_before == slot1_after
    assert slot2_before == slot2_after
    assert slot3_before == slot3_after


def test_finish_deck_play_should_set_remaining_turns():
    gamestate = GameState(get_player_names(5), get_suits(5))
    player = gamestate.players[gamestate.player_turn]
    while len(gamestate.deck) > 1:
        gamestate.deck.pop()

    action = PlayAction(2)
    gamestate.play_turn(action)

    assert gamestate.turns_remaining == len(gamestate.players)


def test_discard_should_add_card_to_discard_pile():
    gamestate = GameState(get_player_names(5), get_suits(5))
    player = gamestate.players[gamestate.player_turn]
    gamestate.current_clues = 4

    slot1_before = player.hand[1].real_card
    slot2_before = player.hand[2].real_card

    assert gamestate.discard_pile.count(slot1_before) == 0
    assert gamestate.discard_pile.count(slot2_before) == 0

    action = DiscardAction(2)
    gamestate.play_turn(action)

    assert gamestate.discard_pile.count(slot1_before) == 0
    assert gamestate.discard_pile.count(slot2_before) == 1
