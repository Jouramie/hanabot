from core.state.status import Status


def test_new_status_should_have_8_clues():
    status = Status()
    assert status.current_clues == 8


def test_new_status_should_be_on_turn_zero():
    status = Status()
    assert status.current_turn == 0


def test_new_status_should_have_zero_strikes():
    status = Status()
    assert status.current_strikes == 0


def test_new_status_should_not_be_over():
    status = Status()
    assert not status.is_over