from bots.domain.model.hand import Hand
from bots.hanabot.conventions import Conventions


def test_when_no_card_clued_then_chop_is_oldest_card(mocker):
    conventions = Conventions()

    chop = conventions.find_chop(
        Hand(
            "jake",
            (mocker.Mock(is_clued=False), mocker.Mock(is_clued=False), mocker.Mock(is_clued=False)),
        )
    )

    assert chop == 2


def test_when_last_card_clued_then_chop_is_on_not_clued_oldest_card(mocker):
    conventions = Conventions()

    chop = conventions.find_chop(
        Hand(
            "logan",
            (mocker.Mock(is_clued=False), mocker.Mock(is_clued=False), mocker.Mock(is_clued=True)),
        )
    )

    assert chop == 1


def test_when_first_card_clued_then_chop_is_on_not_clued_oldest_card(mocker):
    conventions = Conventions()

    chop = conventions.find_chop(
        Hand(
            "logan",
            (mocker.Mock(is_clued=True), mocker.Mock(is_clued=False), mocker.Mock(is_clued=True)),
        )
    )

    assert chop == 1
