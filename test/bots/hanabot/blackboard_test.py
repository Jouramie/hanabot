from bots.domain.model.game_state import GameHistory
from bots.domain.model.hand import Hand, HandCard
from bots.hanabot.blackboard import Blackboard, Interpretation
from core import Card, Suit, Rank, all_possible_cards
from test.bots.domain.model.game_state_test import RelativeGameStateBuilder


def test_given_used_blackboard_when_wipe_for_new_turn_then_reset_state_for_new_turn(mocker):
    blackboard = Blackboard()
    blackboard.current_game_state = mocker.Mock()
    blackboard.current_game_state.turn_number = 3
    blackboard.history = mocker.Mock()
    blackboard.chop = mocker.Mock()
    blackboard.uninterpreted_turns = mocker.Mock()
    blackboard.ongoing_interpretations = "ongoing_interpretations"
    blackboard.resolved_interpretations = "resolved_interpretations"

    new_game_state = mocker.Mock()
    new_history = GameHistory()

    blackboard.wipe_for_new_turn(new_game_state, new_history)

    assert blackboard.current_game_state is new_game_state
    assert blackboard.history is new_history
    assert blackboard.chop is None
    assert blackboard.ongoing_interpretations == "ongoing_interpretations"
    assert blackboard.resolved_interpretations == "resolved_interpretations"


def test_given_empty_blackboard_when_wipe_for_new_turn_then_add_uninterpreted_actions_from_history(mocker):
    blackboard = Blackboard()

    new_game_state = mocker.Mock()
    new_game_state.turn_number = 2

    turn_0 = mocker.Mock()
    turn_1 = mocker.Mock()
    turn_2 = mocker.Mock()
    new_history = GameHistory([turn_0, turn_1, turn_2])

    blackboard.wipe_for_new_turn(new_game_state, new_history)

    assert blackboard.uninterpreted_turns == [turn_0, turn_1, turn_2]


def test_given_used_blackboard_when_wipe_for_new_turn_then_add_uninterpreted_actions_from_history(mocker):
    blackboard = Blackboard()
    blackboard.current_game_state = mocker.Mock()
    blackboard.current_game_state.turn_number = 3

    new_game_state = mocker.Mock()
    new_game_state.turn_number = 5

    turn_3 = mocker.Mock()
    turn_4 = mocker.Mock()
    turn_5 = mocker.Mock()
    new_history = GameHistory([mocker.Mock(), mocker.Mock(), mocker.Mock(), turn_3, turn_4, turn_5])

    blackboard.wipe_for_new_turn(new_game_state, new_history)

    assert blackboard.uninterpreted_turns == [turn_3, turn_4, turn_5]


def test_given_uninterpreted_action_when_write_new_interpretation_then_uninterpreted_action_is_removed(mocker):
    blackboard = Blackboard()
    uninterpreted_turn = mocker.Mock()
    blackboard.uninterpreted_turns = [uninterpreted_turn]

    interpretation = mocker.Mock()
    interpretation.of_turn = uninterpreted_turn
    blackboard.write_new_interpretation(interpretation)

    assert blackboard.uninterpreted_turns == []


def test_given_uninterpreted_action_when_write_new_interpretation_then_ongoing_interpretation_is_added(mocker):
    blackboard = Blackboard()
    blackboard.uninterpreted_turns = mocker.Mock()

    interpretation = mocker.Mock()
    blackboard.write_new_interpretation(interpretation)

    assert blackboard.ongoing_interpretations == [interpretation]


def test_given_ongoing_interpretation_when_write_notes_on_cards_then_concerned_cards_receive_interpretation(mocker):
    blackboard = Blackboard()
    expected_card = Card(Suit.RED, Rank.FIVE)
    blackboard.ongoing_interpretations = [Interpretation(mocker.Mock(), notes_on_cards={0: {expected_card}})]
    blackboard.current_game_state = RelativeGameStateBuilder().set_my_hand(Hand("alfred", (HandCard(all_possible_cards(), True, 0),))).build()

    blackboard.write_notes_on_cards()

    assert blackboard.my_hand[0].notes_on_cards == {expected_card}
