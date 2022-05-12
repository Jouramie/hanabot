from bots.domain.decision import SuitClueDecision, DiscardDecision, PlayDecision
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
        (
            HandCard.create_relative_card(12),
            HandCard.create_relative_card(9),
            HandCard.create_relative_card(6),
            HandCard.create_relative_card(3),
            HandCard.create_relative_card(0),
        ),
    )
    bob_hand = Hand(
        "bob",
        (
            HandCard.create_real_card(13, Card(Suit.RED, Rank.ONE)),
            HandCard.create_real_card(10, Card(Suit.BLUE, Rank.ONE)),
            HandCard.create_real_card(7, Card(Suit.BLUE, Rank.ONE)),
            HandCard.create_real_card(4, Card(Suit.YELLOW, Rank.FOUR)),
            HandCard.create_real_card(1, Card(Suit.YELLOW, Rank.FOUR)),
        ),
    )
    cathy_hand = Hand(
        "cathy",
        (
            HandCard.create_real_card(14, Card(Suit.YELLOW, Rank.FIVE)),
            HandCard.create_real_card(11, Card(Suit.PURPLE, Rank.FOUR)),
            HandCard.create_real_card(8, Card(Suit.BLUE, Rank.FOUR)),
            HandCard.create_real_card(5, Card(Suit.PURPLE, Rank.FIVE)),
            HandCard.create_real_card(2, Card(Suit.RED, Rank.TWO)),
        ),
    )
    current_game_state = (
        RelativeGameStateBuilder()
        .set_my_hand(alice_hand)
        .set_other_player_hands(
            update_cards(bob_hand, HandCard.create_real_card(draw_id=13, card=Card(Suit.RED, Rank.ONE), suit_known=True)),
            cathy_hand,
        )
        .build()
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
        SuitClueAction("bob", frozenset({0}), Suit.RED),
        current_game_state,
    )

    alice = Hanabot(level_one)
    decision = alice.play_turn(current_game_state, GameHistory([previous_turn]))

    assert decision == SuitClueDecision(Suit.RED, 2)


def test_given_clued_one_when_play_turn_then_clue_another_one():
    alice_hand = Hand(
        "alice",
        (
            HandCard.create_relative_card(12),
            HandCard.create_relative_card(9),
            HandCard.create_relative_card(6),
            HandCard.create_relative_card(3),
            HandCard.create_relative_card(0),
        ),
    )
    bob_hand = Hand(
        "bob",
        (
            HandCard.create_real_card(13, Card(Suit.RED, Rank.ONE)),
            HandCard.create_real_card(10, Card(Suit.BLUE, Rank.ONE)),
            HandCard.create_real_card(7, Card(Suit.BLUE, Rank.ONE)),
            HandCard.create_real_card(4, Card(Suit.RED, Rank.FOUR)),
            HandCard.create_real_card(1, Card(Suit.YELLOW, Rank.FOUR)),
        ),
    )
    cathy_hand = Hand(
        "cathy",
        (
            HandCard.create_real_card(14, Card(Suit.YELLOW, Rank.FIVE)),
            HandCard.create_real_card(11, Card(Suit.PURPLE, Rank.FOUR)),
            HandCard.create_real_card(8, Card(Suit.BLUE, Rank.FOUR)),
            HandCard.create_real_card(5, Card(Suit.PURPLE, Rank.FIVE)),
            HandCard.create_real_card(2, Card(Suit.YELLOW, Rank.ONE)),
        ),
    )
    current_game_state = (
        RelativeGameStateBuilder()
        .set_my_hand(alice_hand)
        .set_other_player_hands(
            update_cards(bob_hand, HandCard.create_real_card(draw_id=13, card=Card(Suit.RED, Rank.ONE), suit_known=True)),
            cathy_hand,
        )
        .build()
    )
    previous_turn = Turn(
        RelativeGameStateBuilder()
        .set_my_hand(alice_hand)
        .set_other_player_hands(
            bob_hand,
            cathy_hand,
        )
        .build(),
        SuitClueAction("bob", frozenset({0}), Suit.RED),
        current_game_state,
    )

    alice = Hanabot(level_one)
    decision = alice.play_turn(current_game_state, GameHistory([previous_turn]))

    assert decision == SuitClueDecision(Suit.YELLOW, 2)


def test_given_all_playable_already_clued_when_play_turn_then_discard():
    alice_hand = Hand(
        "alice",
        (
            HandCard.create_relative_card(12),
            HandCard.create_relative_card(9),
            HandCard.create_relative_card(6),
            HandCard.create_relative_card(3),
            HandCard.create_relative_card(0),
        ),
    )
    bob_hand = Hand(
        "bob",
        (
            HandCard.create_real_card(13, Card(Suit.RED, Rank.ONE)),
            HandCard.create_real_card(10, Card(Suit.BLUE, Rank.ONE)),
            HandCard.create_real_card(7, Card(Suit.BLUE, Rank.ONE)),
            HandCard.create_real_card(4, Card(Suit.RED, Rank.FOUR)),
            HandCard.create_real_card(1, Card(Suit.YELLOW, Rank.FOUR)),
        ),
    )
    cathy_hand = Hand(
        "cathy",
        (
            HandCard.create_real_card(14, Card(Suit.YELLOW, Rank.FIVE)),
            HandCard.create_real_card(11, Card(Suit.PURPLE, Rank.FOUR)),
            HandCard.create_real_card(8, Card(Suit.BLUE, Rank.FOUR)),
            HandCard.create_real_card(5, Card(Suit.PURPLE, Rank.FIVE)),
            HandCard.create_real_card(2, Card(Suit.YELLOW, Rank.TWO)),
        ),
    )
    current_game_state = (
        RelativeGameStateBuilder()
        .set_clue_count(4)
        .set_my_hand(alice_hand)
        .set_other_player_hands(
            update_cards(bob_hand, HandCard.create_real_card(draw_id=13, card=Card(Suit.RED, Rank.ONE), suit_known=True)),
            cathy_hand,
        )
        .build()
    )
    previous_turn = Turn(
        RelativeGameStateBuilder()
        .set_my_hand(alice_hand)
        .set_other_player_hands(
            bob_hand,
            cathy_hand,
        )
        .build(),
        SuitClueAction("bob", frozenset({0}), Suit.RED),
        current_game_state,
    )

    alice = Hanabot(level_one)
    decision = alice.play_turn(current_game_state, GameHistory([previous_turn]))

    assert decision == DiscardDecision(4)


def test_given_card_already_prompted_when_play_turn_then_do_not_prompt_again():
    cathy_hand = Hand(
        "cathy",
        (
            HandCard.create_relative_card(15),
            HandCard.create_relative_card(11),
            HandCard.create_relative_card(7),
            HandCard.create_relative_card(3),
        ),
    )
    donald_hand = Hand(
        "donald",
        (
            HandCard.create_real_card(12, Card(Suit.GREEN, Rank.FOUR)),
            HandCard.create_real_card(8, Card(Suit.BLUE, Rank.FOUR)),
            HandCard.create_real_card(4, Card(Suit.GREEN, Rank.TWO)),
            HandCard.create_real_card(0, Card(Suit.PURPLE, Rank.ONE)),
        ),
    )
    alice_hand = Hand(
        "alice",
        (
            HandCard.create_real_card(13, Card(Suit.PURPLE, Rank.TWO)),
            HandCard.create_real_card(9, Card(Suit.RED, Rank.ONE)),
            HandCard.create_real_card(5, Card(Suit.RED, Rank.ONE)),
            HandCard.create_real_card(1, Card(Suit.YELLOW, Rank.FOUR)),
        ),
    )
    bob_hand = Hand(
        "bob",
        (
            HandCard.create_real_card(14, Card(Suit.YELLOW, Rank.FOUR)),
            HandCard.create_real_card(10, Card(Suit.PURPLE, Rank.ONE)),
            HandCard.create_real_card(6, Card(Suit.PURPLE, Rank.ONE)),
            HandCard.create_real_card(2, Card(Suit.PURPLE, Rank.TWO)),
        ),
    )
    second_game_state = (
        RelativeGameStateBuilder()
        .set_clue_count(7)
        .set_my_hand(cathy_hand)
        .set_other_player_hands(
            update_cards(donald_hand, HandCard.create_real_card(0, Card(Suit.PURPLE, Rank.ONE), suit_known=True)),
            alice_hand,
            bob_hand,
        )
        .build()
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
        SuitClueAction("donald", frozenset({3}), Suit.PURPLE),
        second_game_state,
    )
    current_game_state = (
        RelativeGameStateBuilder()
        .set_clue_count(6)
        .set_my_hand(cathy_hand)
        .set_other_player_hands(
            update_cards(donald_hand, HandCard.create_real_card(0, Card(Suit.PURPLE, Rank.ONE), suit_known=True)),
            update_cards(alice_hand, HandCard.create_real_card(13, Card(Suit.PURPLE, Rank.TWO), suit_known=True)),
            bob_hand,
        )
        .build()
    )
    second_turn = Turn(second_game_state, SuitClueAction("alice", frozenset({0}), Suit.PURPLE), current_game_state)

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
        (
            HandCard.create_relative_card(12),
            HandCard.create_relative_card(9),
            HandCard.create_relative_card(6),
            HandCard.create_relative_card(3),
            HandCard.create_relative_card(0, rank=Rank.FIVE),
        ),
    )
    bob_hand = Hand(
        "bob",
        (
            HandCard.create_real_card(13, Card(Suit.RED, Rank.ONE)),
            HandCard.create_real_card(10, Card(Suit.BLUE, Rank.ONE)),
            HandCard.create_real_card(7, Card(Suit.BLUE, Rank.ONE)),
            HandCard.create_real_card(4, Card(Suit.RED, Rank.FOUR)),
            HandCard.create_real_card(1, Card(Suit.YELLOW, Rank.FOUR)),
        ),
    )
    cathy_hand = Hand(
        "cathy",
        (
            HandCard.create_real_card(14, Card(Suit.YELLOW, Rank.FIVE)),
            HandCard.create_real_card(11, Card(Suit.PURPLE, Rank.FOUR)),
            HandCard.create_real_card(8, Card(Suit.BLUE, Rank.FOUR)),
            HandCard.create_real_card(5, Card(Suit.PURPLE, Rank.FIVE)),
            HandCard.create_real_card(2, Card(Suit.YELLOW, Rank.ONE)),
        ),
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
    previous_turn = Turn(
        RelativeGameStateBuilder()
        .set_stacks(stacks)
        .set_my_hand(alice_hand)
        .set_other_player_hands(
            bob_hand,
            cathy_hand,
        )
        .build(),
        RankClueAction("alice", frozenset({4}), Rank.FIVE),
        current_game_state,
    )

    alice = Hanabot(level_one)
    decision = alice.play_turn(current_game_state, GameHistory([previous_turn]))

    assert decision == PlayDecision(4)


def test_given_clue_on_five_on_chop_when_play_turn_then_play_five():
    stacks = Stacks.create_from_dict({Suit.YELLOW: Rank.FOUR})
    alice_hand = Hand(
        "alice",
        (
            HandCard.create_relative_card(12),
            HandCard.create_relative_card(9),
            HandCard.create_relative_card(6),
            HandCard.create_relative_card(3),
            HandCard.create_relative_card(0),
        ),
    )
    bob_hand = Hand(
        "bob",
        (
            HandCard.create_real_card(13, Card(Suit.RED, Rank.ONE)),
            HandCard.create_real_card(10, Card(Suit.BLUE, Rank.ONE)),
            HandCard.create_real_card(7, Card(Suit.BLUE, Rank.ONE)),
            HandCard.create_real_card(4, Card(Suit.RED, Rank.FOUR)),
            HandCard.create_real_card(1, Card(Suit.YELLOW, Rank.FOUR)),
        ),
    )
    cathy_hand = Hand(
        "cathy",
        (
            HandCard.create_real_card(14, Card(Suit.YELLOW, Rank.FIVE)),
            HandCard.create_real_card(11, Card(Suit.PURPLE, Rank.FOUR)),
            HandCard.create_real_card(8, Card(Suit.BLUE, Rank.FOUR)),
            HandCard.create_real_card(5, Card(Suit.PURPLE, Rank.FIVE)),
            HandCard.create_real_card(2, Card(Suit.YELLOW, Rank.ONE)),
        ),
    )
    current_game_state = (
        RelativeGameStateBuilder()
        .set_stacks(stacks)
        .set_my_hand(update_cards(alice_hand, HandCard.create_relative_card(0, rank=Rank.FIVE)))
        .set_other_player_hands(
            bob_hand,
            cathy_hand,
        )
        .build()
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
        RankClueAction("alice", frozenset({4}), Rank.FIVE),
        current_game_state,
    )

    alice = Hanabot(level_one)
    decision = alice.play_turn(current_game_state, GameHistory([previous_turn]))

    assert decision != PlayDecision(4)


def update_cards(hand: Hand, *cards: HandCard) -> Hand:
    cards_to_update = {card.draw_id: card for card in cards}
    updated_cards = []
    for card in hand.cards:
        if card.draw_id in cards_to_update:
            updated_cards.append(cards_to_update[card.draw_id])
        else:
            updated_cards.append(card)

    return Hand(hand.owner_name, tuple(updated_cards))
