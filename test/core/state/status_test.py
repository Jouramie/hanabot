from core.state.status import Status


def test_new_status_should_have_8_clues():
    status = Status(50)
    assert status.clues == 8


def test_new_status_should_be_on_turn_zero():
    status = Status(50)
    assert status.turn == 0


def test_new_status_should_have_zero_strikes():
    status = Status(50)
    assert status.strikes == 0


def test_new_status_should_not_be_over():
    status = Status(50)
    assert not status.is_over


def test_new_status_set_turns_remaining():
    status = Status(50)
    assert status.turns_remaining == 50


def test_next_turn_should_increment_current_turn():
    status = Status(50)
    assert status.turn == 0
    status.next_turn()
    assert status.turn == 1
    status.next_turn()
    assert status.turn == 2


def test_add_strike_should_increment_strikes():
    status = Status(50)
    assert status.strikes == 0
    status.add_strike()
    assert status.strikes == 1
    status.add_strike()
    assert status.strikes == 2
    status.add_strike()
    assert status.strikes == 3


def test_add_third_strike_should_end_the_game():
    status = Status(50)
    assert not status.is_over
    status.add_strike()
    assert not status.is_over
    status.add_strike()
    assert not status.is_over
    status.add_strike()
    assert status.is_over


def test_generate_clue_should_increment_clues():
    status = Status(50)
    status.clues = 4
    status.generate_clue()
    assert status.clues == 5
    status.generate_clue()
    assert status.clues == 6
    status.generate_clue()
    assert status.clues == 7


def test_consume_clue_should_decrement_clues():
    status = Status(50)
    assert status.clues == 8
    status.consume_clue()
    assert status.clues == 7
    status.consume_clue()
    assert status.clues == 6
    status.consume_clue()
    assert status.clues == 5


def test_decrement_turns_should_reduce_by_one():
    status = Status(50)
    assert status.turns_remaining == 50
    status.decrement_turns_remaining()
    assert status.turns_remaining == 49
    status.decrement_turns_remaining()
    status.decrement_turns_remaining()
    assert status.turns_remaining == 47


def test_decrement_turns_should_end_when_zero():
    status = Status(3)
    assert not status.is_over
    status.decrement_turns_remaining()
    assert not status.is_over
    status.decrement_turns_remaining()
    assert not status.is_over
    status.decrement_turns_remaining()
    assert status.is_over
    status.decrement_turns_remaining()
    assert status.is_over

