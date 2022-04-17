from simulator.game.action import ClueAction, PlayAction, DiscardAction
from simulator.game.clue import ColorClue
from test.simulator.game_setup import get_player_names, get_suits

from simulator.game.gamestate import GameState


def test_give_clue_should_use_clue():
    gamestate = GameState(get_player_names(5), get_suits(5))
    second_player = gamestate.players[1]
    second_card = second_player.hand[1]
    clue = ColorClue(second_card.suit, second_player)
    action = ClueAction(clue)

    clues_before_action = gamestate.current_clues
    gamestate.play_turn(action)
    clues_after_action = gamestate.current_clues
    assert clues_before_action == clues_after_action + 1


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


def test_clue_should_not_draw_card():
    gamestate = GameState(get_player_names(5), get_suits(5))
    player = gamestate.players[gamestate.player_turn]

    slot0_before = player.hand[0]
    slot1_before = player.hand[1]
    slot2_before = player.hand[2]
    slot3_before = player.hand[3]

    second_player = gamestate.players[1]
    second_card = second_player.hand[1]
    clue = ColorClue(second_card.suit, second_player)
    action = ClueAction(clue)
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


def test_empty_deck_clue_should_not_draw_card():
    gamestate = GameState(get_player_names(5), get_suits(5))
    player = gamestate.players[gamestate.player_turn]
    gamestate.deck = []

    slot0_before = player.hand[0]
    slot1_before = player.hand[1]
    slot2_before = player.hand[2]
    slot3_before = player.hand[3]

    second_player = gamestate.players[1]
    second_card = second_player.hand[1]
    clue = ColorClue(second_card.suit, second_player)
    action = ClueAction(clue)
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
