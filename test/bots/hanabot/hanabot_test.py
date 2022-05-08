from typing import Iterable

from bots.domain.decision import SuitClueDecision, RankClueDecision, DiscardDecision, PlayDecision
from bots.domain.model.action import SuitClueAction, RankClueAction
from bots.domain.model.game_state import GameHistory, Turn
from bots.domain.model.hand import HandCard, Hand
from bots.hanabot.conventions import level_one
from bots.hanabot.hanabot import Hanabot
from core import Card, Rank, Suit
from core.stack import Stacks
from test.bots.domain.model.game_state_test import RelativeGameStateBuilder


def test_given_clued_one_when_play_turn_then_clue_next():
    alice_hand = Hand(
        "alice",
        (HandCard.unknown_card(12), HandCard.unknown_card(9), HandCard.unknown_card(6), HandCard.unknown_card(3), HandCard.unknown_card(0)),
    )
    bob_hand = Hand(
        "bob",
        (
            HandCard.unknown_real_card(13, Card(Suit.RED, Rank.ONE)),
            HandCard.unknown_real_card(10, Card(Suit.BLUE, Rank.ONE)),
            HandCard.unknown_real_card(7, Card(Suit.BLUE, Rank.ONE)),
            HandCard.unknown_real_card(4, Card(Suit.YELLOW, Rank.FOUR)),
            HandCard.unknown_real_card(1, Card(Suit.YELLOW, Rank.FOUR)),
        ),
    )
    cathy_hand = Hand(
        "cathy",
        (
            HandCard.unknown_real_card(14, Card(Suit.YELLOW, Rank.FIVE)),
            HandCard.unknown_real_card(11, Card(Suit.PURPLE, Rank.FOUR)),
            HandCard.unknown_real_card(8, Card(Suit.BLUE, Rank.FOUR)),
            HandCard.unknown_real_card(5, Card(Suit.PURPLE, Rank.FIVE)),
            HandCard.unknown_real_card(2, Card(Suit.RED, Rank.TWO)),
        ),
    )
    previous_turn = Turn(
        (
            RelativeGameStateBuilder()
            .set_my_hand(alice_hand)
            .set_other_player_hands(
                bob_hand,
                cathy_hand,
            )
            .build()
        ),
        SuitClueAction("bob", frozenset({0}), frozenset({13}), Suit.RED),
    )
    current_game_state = (
        RelativeGameStateBuilder()
        .set_my_hand(alice_hand)
        .set_other_player_hands(
            update_cards(bob_hand, HandCard.clued_real_card(draw_id=13, card=Card(Suit.RED, Rank.ONE), suit_known=True)),
            cathy_hand,
        )
        .build()
    )

    alice = Hanabot(level_one)
    decision = alice.play_turn(current_game_state, GameHistory([previous_turn]))

    assert decision == SuitClueDecision(Suit.RED, 2)


def test_given_clued_one_when_play_turn_then_clue_another_one():
    alice_hand = Hand(
        "alice",
        (HandCard.unknown_card(12), HandCard.unknown_card(9), HandCard.unknown_card(6), HandCard.unknown_card(3), HandCard.unknown_card(0)),
    )
    bob_hand = Hand(
        "bob",
        (
            HandCard.unknown_real_card(13, Card(Suit.RED, Rank.ONE)),
            HandCard.unknown_real_card(10, Card(Suit.BLUE, Rank.ONE)),
            HandCard.unknown_real_card(7, Card(Suit.BLUE, Rank.ONE)),
            HandCard.unknown_real_card(4, Card(Suit.RED, Rank.FOUR)),
            HandCard.unknown_real_card(1, Card(Suit.YELLOW, Rank.FOUR)),
        ),
    )
    cathy_hand = Hand(
        "cathy",
        (
            HandCard.unknown_real_card(14, Card(Suit.YELLOW, Rank.FIVE)),
            HandCard.unknown_real_card(11, Card(Suit.PURPLE, Rank.FOUR)),
            HandCard.unknown_real_card(8, Card(Suit.BLUE, Rank.FOUR)),
            HandCard.unknown_real_card(5, Card(Suit.PURPLE, Rank.FIVE)),
            HandCard.unknown_real_card(2, Card(Suit.YELLOW, Rank.ONE)),
        ),
    )
    previous_turn = Turn(
        RelativeGameStateBuilder()
        .set_my_hand(alice_hand)
        .set_other_player_hands(
            bob_hand,
            cathy_hand,
        )
        .build(),
        SuitClueAction("bob", frozenset({0}), frozenset({13}), Suit.RED),
    )

    current_game_state = (
        RelativeGameStateBuilder()
        .set_my_hand(alice_hand)
        .set_other_player_hands(
            update_cards(bob_hand, HandCard.clued_real_card(draw_id=13, card=Card(Suit.RED, Rank.ONE), suit_known=True)),
            cathy_hand,
        )
        .build()
    )

    alice = Hanabot(level_one)
    decision = alice.play_turn(current_game_state, GameHistory([previous_turn]))

    assert decision == RankClueDecision(Rank.ONE, 2)


def test_given_all_playable_already_clued_when_play_turn_then_discard():
    alice_hand = Hand(
        "alice",
        (HandCard.unknown_card(12), HandCard.unknown_card(9), HandCard.unknown_card(6), HandCard.unknown_card(3), HandCard.unknown_card(0)),
    )
    bob_hand = Hand(
        "bob",
        (
            HandCard.unknown_real_card(13, Card(Suit.RED, Rank.ONE)),
            HandCard.unknown_real_card(10, Card(Suit.BLUE, Rank.ONE)),
            HandCard.unknown_real_card(7, Card(Suit.BLUE, Rank.ONE)),
            HandCard.unknown_real_card(4, Card(Suit.RED, Rank.FOUR)),
            HandCard.unknown_real_card(1, Card(Suit.YELLOW, Rank.FOUR)),
        ),
    )
    cathy_hand = Hand(
        "cathy",
        (
            HandCard.unknown_real_card(14, Card(Suit.YELLOW, Rank.FIVE)),
            HandCard.unknown_real_card(11, Card(Suit.PURPLE, Rank.FOUR)),
            HandCard.unknown_real_card(8, Card(Suit.BLUE, Rank.FOUR)),
            HandCard.unknown_real_card(5, Card(Suit.PURPLE, Rank.FIVE)),
            HandCard.unknown_real_card(2, Card(Suit.YELLOW, Rank.TWO)),
        ),
    )
    previous_turn = Turn(
        RelativeGameStateBuilder()
        .set_my_hand(alice_hand)
        .set_other_player_hands(
            bob_hand,
            cathy_hand,
        )
        .build(),
        SuitClueAction("bob", frozenset({0}), frozenset({13}), Suit.RED),
    )
    current_game_state = (
        RelativeGameStateBuilder()
        .set_clue_count(4)
        .set_my_hand(alice_hand)
        .set_other_player_hands(
            update_cards(bob_hand, HandCard.clued_real_card(draw_id=13, card=Card(Suit.RED, Rank.ONE), suit_known=True)),
            cathy_hand,
        )
        .build()
    )

    alice = Hanabot(level_one)
    decision = alice.play_turn(current_game_state, GameHistory([previous_turn]))

    assert decision == DiscardDecision(4)


def test_given_card_already_prompted_when_play_turn_then_do_not_prompt_again():
    cathy_hand = Hand(
        "cathy",
        (
            HandCard.unknown_card(15),
            HandCard.unknown_card(11),
            HandCard.unknown_card(7),
            HandCard.unknown_card(3),
        ),
    )
    donald_hand = Hand(
        "donald",
        (
            HandCard.unknown_real_card(12, Card(Suit.GREEN, Rank.FOUR)),
            HandCard.unknown_real_card(8, Card(Suit.BLUE, Rank.FOUR)),
            HandCard.unknown_real_card(4, Card(Suit.GREEN, Rank.TWO)),
            HandCard.unknown_real_card(0, Card(Suit.PURPLE, Rank.ONE)),
        ),
    )
    alice_hand = Hand(
        "alice",
        (
            HandCard.unknown_real_card(13, Card(Suit.PURPLE, Rank.TWO)),
            HandCard.unknown_real_card(9, Card(Suit.RED, Rank.ONE)),
            HandCard.unknown_real_card(5, Card(Suit.RED, Rank.ONE)),
            HandCard.unknown_real_card(1, Card(Suit.YELLOW, Rank.FOUR)),
        ),
    )
    bob_hand = Hand(
        "bob",
        (
            HandCard.unknown_real_card(14, Card(Suit.YELLOW, Rank.FOUR)),
            HandCard.unknown_real_card(10, Card(Suit.PURPLE, Rank.ONE)),
            HandCard.unknown_real_card(6, Card(Suit.PURPLE, Rank.ONE)),
            HandCard.unknown_real_card(2, Card(Suit.PURPLE, Rank.TWO)),
        ),
    )
    first_turn = Turn(
        RelativeGameStateBuilder()
        .set_my_hand(cathy_hand)
        .set_other_player_hands(
            donald_hand,
            alice_hand,
            bob_hand,
        )
        .build(),
        SuitClueAction("donald", frozenset({3}), frozenset({0}), Suit.PURPLE),
    )
    second_turn = Turn(
        RelativeGameStateBuilder()
        .set_clue_count(7)
        .set_my_hand(cathy_hand)
        .set_other_player_hands(
            update_cards(donald_hand, HandCard.clued_real_card(0, Card(Suit.PURPLE, Rank.ONE), suit_known=True)),
            alice_hand,
            bob_hand,
        )
        .build(),
        SuitClueAction("alice", frozenset({0}), frozenset({13}), Suit.PURPLE),
    )
    current_game_state = (
        RelativeGameStateBuilder()
        .set_clue_count(6)
        .set_my_hand(cathy_hand)
        .set_other_player_hands(
            update_cards(donald_hand, HandCard.clued_real_card(0, Card(Suit.PURPLE, Rank.ONE), suit_known=True)),
            update_cards(alice_hand, HandCard.clued_real_card(13, Card(Suit.PURPLE, Rank.TWO), suit_known=True)),
            bob_hand,
        )
        .build()
    )

    donald = Hanabot(level_one)
    decision = donald.play_turn(
        current_game_state,
        GameHistory(
            [
                first_turn,
                second_turn,
            ]
        ),
    )

    assert decision == DiscardDecision(3)


def test_given_clue_on_saved_five_when_play_turn_then_play_five():
    stacks = Stacks.create_from_dict({Suit.YELLOW: Rank.FOUR})
    alice_hand = Hand(
        "alice",
        (HandCard.unknown_card(12), HandCard.unknown_card(9), HandCard.unknown_card(6), HandCard.unknown_card(3), HandCard.clued_card(0, rank=Rank.FIVE)),
    )
    bob_hand = Hand(
        "bob",
        (
            HandCard.unknown_real_card(13, Card(Suit.RED, Rank.ONE)),
            HandCard.unknown_real_card(10, Card(Suit.BLUE, Rank.ONE)),
            HandCard.unknown_real_card(7, Card(Suit.BLUE, Rank.ONE)),
            HandCard.unknown_real_card(4, Card(Suit.RED, Rank.FOUR)),
            HandCard.unknown_real_card(1, Card(Suit.YELLOW, Rank.FOUR)),
        ),
    )
    cathy_hand = Hand(
        "cathy",
        (
            HandCard.unknown_real_card(14, Card(Suit.YELLOW, Rank.FIVE)),
            HandCard.unknown_real_card(11, Card(Suit.PURPLE, Rank.FOUR)),
            HandCard.unknown_real_card(8, Card(Suit.BLUE, Rank.FOUR)),
            HandCard.unknown_real_card(5, Card(Suit.PURPLE, Rank.FIVE)),
            HandCard.unknown_real_card(2, Card(Suit.YELLOW, Rank.ONE)),
        ),
    )
    previous_turn = Turn(
        RelativeGameStateBuilder()
        .set_stacks(stacks)
        .set_my_hand(alice_hand)
        .set_other_player_hands(
            bob_hand,
            cathy_hand,
        )
        .build(),
        RankClueAction("alice", frozenset({4}), frozenset({0}), Rank.FIVE),
    )
    current_game_state = (
        RelativeGameStateBuilder()
        .set_stacks(stacks)
        .set_my_hand(alice_hand)
        .set_other_player_hands(
            bob_hand,
            cathy_hand,
        )
        .build()
    )

    alice = Hanabot(level_one)
    decision = alice.play_turn(current_game_state, GameHistory([previous_turn]))

    assert decision == PlayDecision(4)


def test_given_clue_on_five_on_chop_when_play_turn_then_play_five():
    stacks = Stacks.create_from_dict({Suit.YELLOW: Rank.FOUR})
    alice_hand = Hand(
        "alice",
        (HandCard.unknown_card(12), HandCard.unknown_card(9), HandCard.unknown_card(6), HandCard.unknown_card(3), HandCard.unknown_card(0)),
    )
    bob_hand = Hand(
        "bob",
        (
            HandCard.unknown_real_card(13, Card(Suit.RED, Rank.ONE)),
            HandCard.unknown_real_card(10, Card(Suit.BLUE, Rank.ONE)),
            HandCard.unknown_real_card(7, Card(Suit.BLUE, Rank.ONE)),
            HandCard.unknown_real_card(4, Card(Suit.RED, Rank.FOUR)),
            HandCard.unknown_real_card(1, Card(Suit.YELLOW, Rank.FOUR)),
        ),
    )
    cathy_hand = Hand(
        "cathy",
        (
            HandCard.unknown_real_card(14, Card(Suit.YELLOW, Rank.FIVE)),
            HandCard.unknown_real_card(11, Card(Suit.PURPLE, Rank.FOUR)),
            HandCard.unknown_real_card(8, Card(Suit.BLUE, Rank.FOUR)),
            HandCard.unknown_real_card(5, Card(Suit.PURPLE, Rank.FIVE)),
            HandCard.unknown_real_card(2, Card(Suit.YELLOW, Rank.ONE)),
        ),
    )
    previous_turn = Turn(
        RelativeGameStateBuilder()
        .set_stacks(stacks)
        .set_my_hand(alice_hand)
        .set_other_player_hands(
            bob_hand,
            cathy_hand,
        )
        .build(),
        RankClueAction("alice", frozenset({4}), frozenset({0}), Rank.FIVE),
    )
    current_game_state = (
        RelativeGameStateBuilder()
        .set_stacks(stacks)
        .set_my_hand(update_cards(alice_hand, HandCard.clued_card(0, rank=Rank.FIVE)))
        .set_other_player_hands(
            bob_hand,
            cathy_hand,
        )
        .build()
    )

    alice = Hanabot(level_one)
    decision = alice.play_turn(current_game_state, GameHistory([previous_turn]))

    assert decision != PlayDecision(4)


def update_cards(hand: Hand, cards: HandCard | Iterable[HandCard]) -> Hand:
    if isinstance(cards, HandCard):
        cards = [cards]
    cards_to_update = {card.draw_id: card for card in cards}
    updated_cards = []
    for card in hand.cards:
        if card.draw_id in cards_to_update:
            updated_cards.append(cards_to_update[card.draw_id])
        else:
            updated_cards.append(card)

    return Hand(hand.owner_name, tuple(updated_cards))
