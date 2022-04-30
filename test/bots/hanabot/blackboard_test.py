from bots.domain.model.game_state import GameHistory
from bots.domain.model.hand import Hand, HandCard
from bots.hanabot.blackboard import Blackboard, Interpretation
from core import Card, Suit, Rank, all_possible_cards


def test_given_used_blackboard_when_wipe_for_new_turn_then_reset_state_for_new_turn(mocker):
    blackboard = Blackboard()
    blackboard.current_game_state = mocker.Mock()
    blackboard.current_game_state.turn_number = 3
    blackboard.history = mocker.Mock()
    blackboard.chop = mocker.Mock()
    blackboard.uninterpreted_actions = mocker.Mock()
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

    new_history = mocker.Mock()
    action_turn_0 = mocker.Mock()
    action_turn_1 = mocker.Mock()
    action_turn_2 = mocker.Mock()
    new_history.action_history = [action_turn_0, action_turn_1, action_turn_2]

    blackboard.wipe_for_new_turn(new_game_state, new_history)

    assert blackboard.uninterpreted_actions == [action_turn_0, action_turn_1, action_turn_2]


def test_given_used_blackboard_when_wipe_for_new_turn_then_add_uninterpreted_actions_from_history(mocker):
    blackboard = Blackboard()
    blackboard.current_game_state = mocker.Mock()
    blackboard.current_game_state.turn_number = 2

    new_game_state = mocker.Mock()
    new_game_state.turn_number = 5

    new_history = mocker.Mock()
    action_turn_3 = mocker.Mock()
    action_turn_4 = mocker.Mock()
    action_turn_5 = mocker.Mock()
    new_history.action_history = [mocker.Mock(), mocker.Mock(), mocker.Mock(), action_turn_3, action_turn_4, action_turn_5]

    blackboard.wipe_for_new_turn(new_game_state, new_history)

    assert blackboard.uninterpreted_actions == [action_turn_3, action_turn_4, action_turn_5]


def test_given_uninterpreted_action_when_write_new_interpretation_then_uninterpreted_action_is_removed(mocker):
    blackboard = Blackboard()
    uninterpreted_action = mocker.Mock()
    blackboard.uninterpreted_actions = [uninterpreted_action]

    interpretation = mocker.Mock()
    interpretation.of_action = uninterpreted_action
    blackboard.write_new_interpretation(interpretation)

    assert blackboard.uninterpreted_actions == []


def test_given_uninterpreted_action_when_write_new_interpretation_then_ongoing_interpretation_is_added(mocker):
    blackboard = Blackboard()
    blackboard.uninterpreted_actions = mocker.Mock()

    interpretation = mocker.Mock()
    blackboard.write_new_interpretation(interpretation)

    assert blackboard.ongoing_interpretations == [interpretation]


def test_given_ongoing_interpretation_when_write_notes_on_cards_then_concerned_cards_receive_interpretation(mocker):
    blackboard = Blackboard()
    expected_card = Card(Suit.RED, Rank.FIVE)
    blackboard.ongoing_interpretations = [Interpretation(mocker.Mock(), notes_on_cards={0: {expected_card}})]
    blackboard.current_game_state = mocker.Mock()
    blackboard.current_game_state.my_hand = Hand("alfred", (HandCard(frozenset(all_possible_cards()), True, 0),))

    blackboard.write_notes_on_cards()

    assert blackboard.my_hand[0].notes_on_cards == {expected_card}
