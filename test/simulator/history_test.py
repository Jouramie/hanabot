from simulator.game.history import History


def test_new_history_should_have_no_actions():
    history = History()
    assert len(history.actions) == 0


def test_new_history_should_have_no_clues():
    history = History()
    assert len(history.clues) == 0

