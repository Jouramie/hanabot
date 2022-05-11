from bots.domain.decision import SuitClueDecision
from bots.domain.model.action import SuitClueAction
from bots.domain.model.game_state import Turn
from bots.domain.model.hand import Hand, HandCard
from bots.hanabot.blackboard import Interpretation, InterpretationType
from bots.hanabot.conventions import ConventionDocument, PlayClue
from bots.hanabot.conventions.basic.prompt import Prompt
from core import Suit, Card, Rank
from core.stack import Stacks
from test.bots.domain.model.game_state_test import RelativeGameStateBuilder


def test_given_clue_in_my_hand_and_next_playable_already_clues_when_interpret_clue_then_clued_card_is_interpreted_as_next_playable():
    clue = SuitClueAction("cathy", frozenset({1}), Suit.RED)
    game_state = (
        RelativeGameStateBuilder()
        .set_stacks(Stacks.create_from_dict({Suit.RED: Rank.TWO}))
        .set_my_hand(
            Hand(
                "cathy",
                (
                    HandCard.create_relative_card(0),
                    HandCard.create_relative_card(5),
                    HandCard.create_relative_card(0),
                ),
            )
        )
        .set_other_player_hands(
            Hand.create_unknown_hand("alice", 3),
            Hand(
                "bob",
                (
                    HandCard.create_relative_card(0),
                    HandCard.create_real_card(4, Card(Suit.RED, Rank.THREE), suit_known=True),
                    HandCard.create_relative_card(0),
                ),
            ),
        )
        .build()
    )
    turn = Turn(game_state, clue)

    convention = Prompt()
    interpretation = convention.find_interpretation(turn)

    assert interpretation == Interpretation(
        turn,
        interpretation_type=InterpretationType.PLAY,
        explanation=convention.name,
        notes_on_cards={4: {Card(Suit.RED, Rank.THREE)}, 5: {Card(Suit.RED, Rank.FOUR)}},
    )


def test_given_unplayable_clue_in_other_hand_and_same_suit_clued_in_my_hand_when_interpret_clue_then_clued_card_is_interpreted_as_next_playable():
    clue = SuitClueAction("cathy", frozenset({1}), Suit.RED)
    game_state = (
        RelativeGameStateBuilder()
        .set_stacks(Stacks.create_from_dict({Suit.RED: Rank.TWO}))
        .set_my_hand(
            Hand(
                "bob",
                (
                    HandCard.create_relative_card(0),
                    HandCard.create_relative_card(4, suit=Suit.RED),
                    HandCard.create_relative_card(0),
                ),
            )
        )
        .set_other_player_hands(
            Hand(
                "cathy",
                (
                    HandCard.create_relative_card(0),
                    HandCard.create_real_card(5, Card(Suit.RED, Rank.FOUR)),
                    HandCard.create_relative_card(0),
                ),
            ),
            Hand.create_unknown_hand("alice", 3),
        )
        .build()
    )
    turn = Turn(game_state, clue)

    convention = Prompt()
    interpretation = convention.find_interpretation(turn)

    assert interpretation == Interpretation(
        turn,
        interpretation_type=InterpretationType.PLAY,
        explanation=convention.name,
        notes_on_cards={4: {Card(Suit.RED, Rank.THREE)}, 5: {Card(Suit.RED, Rank.FOUR)}},
    )


def test_given_i_sent_prompt_when_interpret_clue_then_prompt_is_correctly_interpreted():
    clue = SuitClueAction("cathy", frozenset({1}), Suit.RED)

    game_state = (
        RelativeGameStateBuilder()
        .set_stacks(Stacks.create_from_dict({Suit.RED: Rank.TWO}))
        .set_my_hand(
            Hand.create_unknown_hand("alice", 3),
        )
        .set_other_player_hands(
            Hand(
                "bob",
                (
                    HandCard.create_relative_card(0),
                    HandCard.create_real_card(4, Card(Suit.RED, Rank.THREE), suit_known=True),
                    HandCard.create_relative_card(0),
                ),
            ),
            Hand(
                "cathy",
                (
                    HandCard.create_relative_card(0),
                    HandCard.create_real_card(5, Card(Suit.RED, Rank.FOUR)),
                    HandCard.create_relative_card(0),
                ),
            ),
        )
        .build()
    )
    turn = Turn(game_state, clue)

    convention = Prompt()
    interpretation = convention.find_interpretation(turn)

    assert interpretation == Interpretation(
        turn,
        interpretation_type=InterpretationType.PLAY,
        explanation=convention.name,
        notes_on_cards={4: {Card(Suit.RED, Rank.THREE)}, 5: {Card(Suit.RED, Rank.FOUR)}},
    )


def test_given_clue_in_my_hand_and_two_next_playable_already_clues_when_interpret_clue_then_clued_card_is_interpreted_as_next_playable():
    clue = SuitClueAction("cathy", frozenset({1}), Suit.RED)
    game_state = (
        RelativeGameStateBuilder()
        .set_stacks(Stacks.create_from_dict({Suit.RED: Rank.ONE}))
        .set_my_hand(
            Hand(
                "cathy",
                (
                    HandCard.create_relative_card(4),
                    HandCard.create_relative_card(5),
                    HandCard.create_relative_card(6),
                ),
            )
        )
        .set_other_player_hands(
            Hand.create_unknown_hand("alice", 3),
            Hand(
                "bob",
                (
                    HandCard.create_real_card(1, Card(Suit.RED, Rank.TWO), suit_known=True),
                    HandCard.create_real_card(2, Card(Suit.RED, Rank.THREE), suit_known=True),
                    HandCard.create_relative_card(3),
                ),
            ),
        )
        .build()
    )

    turn = Turn(game_state, clue)

    convention = Prompt()
    interpretation = convention.find_interpretation(turn)

    assert interpretation == Interpretation(
        turn,
        interpretation_type=InterpretationType.PLAY,
        explanation=convention.name,
        notes_on_cards={1: {Card(Suit.RED, Rank.TWO)}, 2: {Card(Suit.RED, Rank.THREE)}, 5: {Card(Suit.RED, Rank.FOUR)}},
    )


def test_given_unplayable_clue_in_other_hand_and_same_suit_two_clued_in_my_hand_when_interpret_clue_then_clued_card_is_interpreted_as_next_playable():
    clue = SuitClueAction("cathy", frozenset({1}), Suit.RED)
    game_state = (
        RelativeGameStateBuilder()
        .set_stacks(Stacks.create_from_dict({Suit.RED: Rank.ONE}))
        .set_my_hand(
            Hand(
                "bob",
                (
                    HandCard.create_relative_card(1, suit=Suit.RED),
                    HandCard.create_relative_card(2, suit=Suit.RED),
                    HandCard.create_relative_card(3),
                ),
            )
        )
        .set_other_player_hands(
            Hand(
                "cathy",
                (
                    HandCard.create_relative_card(4),
                    HandCard.create_real_card(5, Card(Suit.RED, Rank.FOUR)),
                    HandCard.create_relative_card(6),
                ),
            ),
            Hand.create_unknown_hand("alice", 3),
        )
        .build()
    )
    turn = Turn(game_state, clue)

    convention = Prompt()
    interpretation = convention.find_interpretation(turn)

    assert interpretation == Interpretation(
        turn,
        interpretation_type=InterpretationType.PLAY,
        explanation=convention.name,
        notes_on_cards={1: {Card(Suit.RED, Rank.TWO)}, 2: {Card(Suit.RED, Rank.THREE)}, 5: {Card(Suit.RED, Rank.FOUR)}},
    )


def test_given_playable_card_clued_and_next_playable_accessible_when_find_play_clue_then_clue_next_playable():
    not_fully_known_playable = HandCard.create_real_card(draw_id=4, card=Card(Suit.RED, Rank.THREE), suit_known=True)
    game_state = (
        RelativeGameStateBuilder()
        .set_stacks(Stacks.create_from_dict({Suit.RED: Rank.TWO}))
        .set_my_hand(
            Hand.create_unknown_hand("alice", 3),
        )
        .set_other_player_hands(
            Hand(
                "bob",
                (
                    HandCard.create_real_card(0, Card(Suit.YELLOW, Rank.THREE)),
                    not_fully_known_playable,
                    HandCard.create_real_card(0, Card(Suit.YELLOW, Rank.THREE)),
                ),
            ),
            Hand(
                "cathy",
                (
                    HandCard.create_real_card(0, Card(Suit.BLUE, Rank.FOUR)),
                    HandCard.create_real_card(draw_id=5, card=Card(Suit.RED, Rank.FOUR)),
                    HandCard.create_real_card(0, Card(Suit.BLUE, Rank.THREE)),
                ),
            ),
        )
        .build()
    )

    prompt = Prompt()
    ConventionDocument(play_conventions=[prompt, PlayClue()])
    decision = prompt.find_clue((1, 1, not_fully_known_playable), game_state)

    assert decision == [SuitClueDecision(Suit.RED, 2)]
