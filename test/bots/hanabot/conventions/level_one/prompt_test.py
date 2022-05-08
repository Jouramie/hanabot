from bots.domain.decision import SuitClueDecision
from bots.domain.model.action import SuitClueAction
from bots.domain.model.game_state import Turn
from bots.domain.model.hand import Hand, HandCard
from bots.domain.model.stack import Stacks
from bots.hanabot.blackboard import Interpretation, InterpretationType
from bots.hanabot.conventions import ConventionDocument, SingleCardPlayClue
from bots.hanabot.conventions.basic.prompt import Prompt
from core import Suit, Card, Rank
from test.bots.domain.model.game_state_test import RelativeGameStateBuilder


def test_given_clue_in_my_hand_and_next_playable_already_clues_when_interpret_clue_then_clued_card_is_interpreted_as_next_playable():
    clue = SuitClueAction("cathy", frozenset({1}), frozenset({5}), Suit.RED)
    expected_card = Card(Suit.RED, Rank.FOUR)

    game_state = (
        RelativeGameStateBuilder()
        .set_stacks(Stacks.create_from_dict({Suit.RED: Rank.TWO}))
        .set_my_hand(
            Hand(
                "cathy",
                (
                    HandCard.unknown_card(0),
                    HandCard.unknown_card(5),
                    HandCard.unknown_card(0),
                ),
            )
        )
        .set_other_player_hands(
            Hand.create_unknown_hand("alice", 3),
            Hand(
                "bob",
                (
                    HandCard.unknown_card(0),
                    HandCard.clued_real_card(0, Card(Suit.RED, Rank.THREE), suit_known=True),
                    HandCard.unknown_card(0),
                ),
            ),
        )
        .build()
    )
    turn = Turn(game_state, clue)

    convention = Prompt()
    interpretation = convention.find_interpretation(turn)

    assert interpretation == Interpretation(turn, interpretation_type=InterpretationType.PLAY, explanation=convention.name, notes_on_cards={5: {expected_card}})


def test_given_unplayable_clue_in_other_hand_and_same_suit_clued_in_my_hand_when_interpret_clue_then_clued_card_is_interpreted_as_next_playable():
    clue = SuitClueAction("cathy", frozenset({1}), frozenset({5}), Suit.RED)
    expected_card = Card(Suit.RED, Rank.THREE)

    game_state = (
        RelativeGameStateBuilder()
        .set_stacks(Stacks.create_from_dict({Suit.RED: Rank.TWO}))
        .set_my_hand(
            Hand(
                "bob",
                (
                    HandCard.unknown_card(0),
                    HandCard.clued_card(draw_id=4, suit=Suit.RED),
                    HandCard.unknown_card(0),
                ),
            )
        )
        .set_other_player_hands(
            Hand(
                "cathy",
                (
                    HandCard.unknown_card(0),
                    HandCard.unknown_real_card(5, Card(Suit.RED, Rank.FOUR)),
                    HandCard.unknown_card(0),
                ),
            ),
            Hand.create_unknown_hand("alice", 3),
        )
        .build()
    )
    turn = Turn(game_state, clue)

    convention = Prompt()
    interpretation = convention.find_interpretation(turn)

    assert interpretation == Interpretation(turn, interpretation_type=InterpretationType.PLAY, explanation=convention.name, notes_on_cards={4: {expected_card}})


def test_given_i_sent_prompt_when_interpret_clue_then_prompt_is_correctly_interpreted():
    clue = SuitClueAction("cathy", frozenset({1}), frozenset({5}), Suit.RED)

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
                    HandCard.unknown_card(0),
                    HandCard.clued_real_card(draw_id=4, card=Card(Suit.RED, Rank.THREE), suit_known=True),
                    HandCard.unknown_card(0),
                ),
            ),
            Hand(
                "cathy",
                (
                    HandCard.unknown_card(0),
                    HandCard.unknown_real_card(5, Card(Suit.RED, Rank.FOUR)),
                    HandCard.unknown_card(0),
                ),
            ),
        )
        .build()
    )
    turn = Turn(game_state, clue)

    convention = Prompt()
    interpretation = convention.find_interpretation(turn)

    assert interpretation == Interpretation(
        turn, interpretation_type=InterpretationType.PLAY, explanation=convention.name, notes_on_cards={5: {Card(Suit.RED, Rank.FOUR)}}
    )


def test_given_playable_card_clued_and_next_playable_accessible_when_find_play_clue_then_clue_next_playable():
    not_fully_known_playable = HandCard.clued_real_card(draw_id=4, card=Card(Suit.RED, Rank.THREE), suit_known=True)
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
                    HandCard.unknown_real_card(0, Card(Suit.YELLOW, Rank.THREE)),
                    not_fully_known_playable,
                    HandCard.unknown_real_card(0, Card(Suit.YELLOW, Rank.THREE)),
                ),
            ),
            Hand(
                "cathy",
                (
                    HandCard.unknown_real_card(0, Card(Suit.BLUE, Rank.THREE)),
                    HandCard.unknown_real_card(draw_id=5, card=Card(Suit.RED, Rank.FOUR)),
                    HandCard.unknown_real_card(0, Card(Suit.BLUE, Rank.THREE)),
                ),
            ),
        )
        .build()
    )

    prompt = Prompt()
    ConventionDocument(play_conventions=[prompt, SingleCardPlayClue()])
    decision = prompt.find_clue((1, 1, not_fully_known_playable), game_state)

    assert decision == [SuitClueDecision(Suit.RED, 2)]
