from bots.domain.model.action import RankClueAction
from bots.domain.model.hand import Hand, HandCard
from bots.hanabot.blackboard import Interpretation, InterpretationType
from bots.hanabot.conventions import FiveSave
from core import Rank
from test.bots.domain.model.game_state_test import RelativeGameStateBuilder


def test_given_five_on_chop_when_clue_then_is_interpreted_as_save():
    clue = RankClueAction("alice", frozenset({0}), frozenset({3}), Rank.FIVE)

    game_state = (
        RelativeGameStateBuilder()
        .set_my_hand(
            Hand(
                "alice",
                (
                    HandCard.unknown_card(),
                    HandCard.unknown_card(),
                    HandCard.clued_card(rank=Rank.FIVE, draw_id=10),
                ),
            )
        )
        .set_other_player_hands(
            Hand.create_unknown_hand("bob", 3),
            Hand.create_unknown_hand("cathy", 3),
        )
        .build()
    )

    convention = FiveSave()
    interpretation = convention.find_interpretation(clue, game_state)

    assert interpretation == Interpretation(clue, interpretation_type=InterpretationType.SAVE, explanation=convention.name)


def test_given_five_not_on_chop_when_clue_then_do_not_interpret():
    clue = RankClueAction("alice", frozenset({0}), frozenset({3}), Rank.FIVE)

    game_state = (
        RelativeGameStateBuilder()
        .set_my_hand(
            Hand(
                "alice",
                (
                    HandCard.unknown_card(),
                    HandCard.clued_card(rank=Rank.FIVE, draw_id=10),
                    HandCard.unknown_card(),
                ),
            )
        )
        .set_other_player_hands(
            Hand.create_unknown_hand("bob", 3),
            Hand.create_unknown_hand("cathy", 3),
        )
        .build()
    )

    convention = FiveSave()
    interpretation = convention.find_interpretation(clue, game_state)

    assert interpretation is None
