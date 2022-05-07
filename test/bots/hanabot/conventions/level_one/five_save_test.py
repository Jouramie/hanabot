from bots.domain.model.action import RankClueAction
from bots.domain.model.game_state import Turn
from bots.domain.model.hand import Hand, HandCard
from bots.hanabot.blackboard import Interpretation, InterpretationType
from bots.hanabot.conventions import FiveSave, ConventionDocument
from core import Rank
from test.bots.domain.model.game_state_test import RelativeGameStateBuilder


def test_given_five_on_chop_when_clue_then_is_interpreted_as_save():
    clue = RankClueAction("alice", frozenset({2}), frozenset({3}), Rank.FIVE)

    game_state = (
        RelativeGameStateBuilder()
        .set_my_hand(
            Hand(
                "alice",
                (
                    HandCard.unknown_card(0),
                    HandCard.unknown_card(0),
                    HandCard.unknown_card(3),
                ),
            )
        )
        .set_other_player_hands(
            Hand.create_unknown_hand("bob", 3),
            Hand.create_unknown_hand("cathy", 3),
        )
        .build()
    )
    turn = Turn(game_state, clue)

    convention = FiveSave()
    convention.document = ConventionDocument()
    interpretation = convention.find_interpretation(turn)

    assert interpretation == Interpretation(turn, interpretation_type=InterpretationType.SAVE, explanation=convention.name)


def test_given_five_not_on_chop_when_clue_then_do_not_interpret():
    clue = RankClueAction("alice", frozenset({1}), frozenset({3}), Rank.FIVE)

    game_state = (
        RelativeGameStateBuilder()
        .set_my_hand(
            Hand(
                "alice",
                (
                    HandCard.unknown_card(0),
                    HandCard.unknown_card(3),
                    HandCard.unknown_card(0),
                ),
            )
        )
        .set_other_player_hands(
            Hand.create_unknown_hand("bob", 3),
            Hand.create_unknown_hand("cathy", 3),
        )
        .build()
    )
    turn = Turn(game_state, clue)

    convention = FiveSave()
    convention.document = ConventionDocument()
    interpretation = convention.find_interpretation(turn)

    assert interpretation is None
