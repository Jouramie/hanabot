from bots.domain.model.clue import RankClue
from bots.domain.model.player import PlayerCard
from bots.hanabot.conventions import SingleCardRankPlayClueConvention
from bots.hanabot.conventions.convention import Interpretation, InterpretationType
from core import Rank, all_possible_cards, Card, Suit


def test_given_one_one_left_to_play_when_find_interpretation_then_only_possible_card_is_one_left_to_play(mocker):
    clue = RankClue(frozenset({0}), Rank.ONE)
    expected_card = Card(Suit.GREEN, Rank.ONE)

    game_state = mocker.Mock()
    game_state.my_hand = [PlayerCard(frozenset(all_possible_cards(ranks=Rank.ONE)), True, 0)]
    game_state.is_playable = lambda card: card == expected_card

    convention = SingleCardRankPlayClueConvention()
    interpretation = convention.find_interpretation(clue, game_state)

    assert interpretation == Interpretation(InterpretationType.PLAY, convention.name, {0: {expected_card}})


def test_given_only_multiple_four_playable_when_find_interpretation_then_only_possible_card_is_playable_four(mocker):
    clue = RankClue(frozenset({0}), Rank.ONE)
    expected_cards = {Card(Suit.GREEN, Rank.FOUR), Card(Suit.RED, Rank.FOUR)}

    game_state = mocker.Mock()
    game_state.my_hand = [PlayerCard(frozenset(all_possible_cards(ranks=Rank.FOUR)), True, 0)]
    game_state.is_playable = lambda card: card in expected_cards

    convention = SingleCardRankPlayClueConvention()
    interpretation = convention.find_interpretation(clue, game_state)

    assert interpretation == Interpretation(InterpretationType.PLAY, convention.name, {0: expected_cards})
