from bots.domain.model.action import SuitClueAction, RankClueAction
from bots.domain.model.hand import HandCard, Hand
from bots.hanabot.blackboard import Interpretation, InterpretationType
from bots.hanabot.conventions import SingleCardRankPlayClueConvention
from core import Rank, all_possible_cards, Card, Suit

ME = "alice"


def test_given_one_one_left_to_play_when_find_interpretation_then_only_possible_card_is_one_left_to_play(mocker):
    clue = RankClueAction(ME, frozenset({0}), Rank.ONE)
    expected_card = Card(Suit.GREEN, Rank.ONE)

    game_state = mocker.Mock()
    game_state.my_hand = Hand(ME, (HandCard(frozenset(all_possible_cards(ranks=Rank.ONE)), True, 0),))
    game_state.is_playable = lambda card: card == expected_card

    convention = SingleCardRankPlayClueConvention()
    interpretation = convention.find_interpretation(clue, game_state)

    assert interpretation == Interpretation(
        clue, interpretation_type=InterpretationType.PLAY, convention_name=convention.name, notes_on_cards={0: {expected_card}}
    )


def test_given_only_multiple_four_playable_when_find_interpretation_then_only_possible_card_is_playable_four(mocker):
    clue = RankClueAction(ME, frozenset({0}), Rank.ONE)
    expected_cards = {Card(Suit.GREEN, Rank.FOUR), Card(Suit.RED, Rank.FOUR)}

    game_state = mocker.Mock()
    game_state.my_hand = Hand(ME, (HandCard(frozenset(all_possible_cards(ranks=Rank.FOUR)), True, 0),))
    game_state.is_playable = lambda card: card in expected_cards

    convention = SingleCardRankPlayClueConvention()
    interpretation = convention.find_interpretation(clue, game_state)

    assert interpretation == Interpretation(
        clue, interpretation_type=InterpretationType.PLAY, convention_name=convention.name, notes_on_cards={0: expected_cards}
    )


def test_given_suit_clue_when_find_interpretation_then_do_not_find_interpretation(mocker):
    clue = SuitClueAction("alice", frozenset({0}), Suit.BLUE)

    convention = SingleCardRankPlayClueConvention()
    interpretation = convention.find_interpretation(clue, mocker.Mock())

    assert interpretation is None
