from bots.domain.model.game_state import GameHistory
from bots.domain.model.hand import Hand
from bots.ui.simulator import add_recent_turns_to_history, assemble_relative_game_state
from core import Rank
from simulator.game.action import RankClueAction, PlayAction, DiscardAction
from simulator.game.clue import RankClue
from simulator.game.player import Player


def test_given_cached_hand_when_alice_receives_a_clue_then_bust_alice_cached_hand(mocker):
    cached_hand = Hand("alice", ())
    hand_cache = {"alice": cached_hand}
    history = GameHistory()
    game = mocker.MagicMock()
    gamestate = mocker.MagicMock()
    alice_hand = mocker.MagicMock()
    alice_hand.name = "alice"
    gamestate.players = [alice_hand]
    game.history.gamestates = [gamestate]
    action = RankClueAction(Rank.TWO, Player("alice", []))
    action.turn = 0
    game.history.actions = [action]
    game.history.clues = [RankClue(Rank.TWO, "alice", "bob", 0)]
    game.current_state = gamestate

    add_recent_turns_to_history(history, game, "alice", hand_cache)

    assert hand_cache["alice"] is not cached_hand


def test_given_cached_hand_when_alice_plays_then_bust_alice_cached_hand(mocker):
    cached_hand = Hand("alice", ())
    hand_cache = {"alice": cached_hand}
    history = GameHistory()
    game = mocker.MagicMock()
    gamestate = mocker.MagicMock()
    alice_hand = mocker.MagicMock()
    alice_hand.name = "alice"
    gamestate.players = [alice_hand]
    game.history.gamestates = [gamestate]
    action = PlayAction(0)
    action.actor = mocker.MagicMock()
    action.actor.name = "alice"
    action.drawId = 0
    action.playedCard = mocker.MagicMock()
    game.history.actions = [action]
    game.current_state = gamestate

    add_recent_turns_to_history(history, game, "alice", hand_cache)

    assert hand_cache["alice"] is not cached_hand


def test_given_cached_hand_when_alice_discards_then_bust_alice_cached_hand(mocker):
    cached_hand = Hand("alice", ())
    hand_cache = {"alice": cached_hand}
    history = GameHistory()
    game = mocker.MagicMock()
    gamestate = mocker.MagicMock()
    alice_hand = mocker.MagicMock()
    alice_hand.name = "alice"
    gamestate.players = [alice_hand]
    game.history.gamestates = [gamestate]
    action = DiscardAction(0)
    action.actor = mocker.MagicMock()
    action.actor.name = "alice"
    action.drawId = 0
    action.discardedCard = mocker.MagicMock()
    game.history.actions = [action]
    game.current_state = gamestate

    add_recent_turns_to_history(history, game, "alice", hand_cache)

    assert hand_cache["alice"] is not cached_hand


def test_given_cached_hand_when_assemble_alice_hand_then_used_cached(mocker):
    cached_hand = Hand("alice", ())
    hand_cache = {"alice": cached_hand}
    history = GameHistory()
    game = mocker.MagicMock()
    gamestate = mocker.MagicMock()
    alice_hand = mocker.MagicMock()
    alice_hand.name = "alice"
    gamestate.players = [alice_hand]
    game.history.gamestates = [gamestate]
    action = DiscardAction(0)
    action.actor = mocker.MagicMock()
    action.actor.name = "bob"
    action.drawId = 0
    action.discardedCard = mocker.MagicMock()
    game.history.actions = [action]
    game.current_state = gamestate

    add_recent_turns_to_history(history, game, "alice", hand_cache)

    assert history.turns[-1].previous_game_state.my_hand is cached_hand


def test_given_not_cached_hand_when_assemble_alice_hand_then_add_hand_to_cache(mocker):
    hand_cache = {}
    gamestate = mocker.MagicMock()
    alice_hand = mocker.MagicMock()
    alice_hand.name = "alice"
    gamestate.players = [alice_hand]

    assemble_relative_game_state(gamestate, "alice", hand_cache)

    assert "alice" in hand_cache
