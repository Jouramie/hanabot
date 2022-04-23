from core.state.status import Status


def test_new_status_should_have_8_clues():
    status = Status()
    assert status.clues == 8


def test_new_status_should_be_on_turn_zero():
    status = Status()
    assert status.turn == 0


def test_new_status_should_have_zero_strikes():
    status = Status()
    assert status.strikes == 0


def test_new_status_should_not_be_over():
    status = Status()
    assert not status.is_over


def test_next_turn_should_increment_current_turn():
    status = Status()
    assert status.turn == 0
    status.next_turn()
    assert status.turn == 1
    status.next_turn()
    assert status.turn == 2


def test_add_strike_should_increment_strikes():
    status = Status()
    assert status.strikes == 0
    status.add_strike()
    assert status.strikes == 1
    status.add_strike()
    assert status.strikes == 2
    status.add_strike()
    assert status.strikes == 3


def test_add_third_strike_should_end_the_game():
    status = Status()
    assert not status.is_over
    status.add_strike()
    assert not status.is_over
    status.add_strike()
    assert not status.is_over
    status.add_strike()
    assert status.is_over


def test_generate_clue_should_increment_clues():
    status = Status()
    status.clues = 4
    status.generate_clue()
    assert status.clues == 5
    status.generate_clue()
    assert status.clues == 6
    status.generate_clue()
    assert status.clues == 7


def test_consume_clue_should_decrement_clues():
    status = Status()
    assert status.clues == 8
    status.consume_clue()
    assert status.clues == 7
    status.consume_clue()
    assert status.clues == 6
    status.consume_clue()
    assert status.clues == 5
