from dataclasses import dataclass, field
from typing import List, Iterable, Dict

from bots.domain.model.action import Action
from bots.domain.model.player import PlayerHand, PlayerCard, RelativePlayerId
from bots.domain.model.stack import Stacks
from core import Card, Rank


@dataclass(frozen=True)
class RelativeGameState:
    stacks: Stacks
    discard: tuple[Card, ...]
    player_hands: tuple[PlayerHand, ...]
    last_performed_action: Action | None
    turn_number: int
    clue_count: int
    bomb_count: int

    def is_first_turn(self):
        return self.last_performed_action is None

    def is_critical(self, card: Card) -> bool:
        # TODO should take into account that card could be unplayable because of the discard
        if card.rank is Rank.FIVE:
            return True

        if card.rank is Rank.ONE:
            return self.discard.count(card) == 2

        return card in self.discard

    def find_playable_cards(self) -> Iterable[tuple[RelativePlayerId, int, PlayerCard]]:
        for relative_player_id, hand in enumerate(self.other_player_hands, 1):
            for slot, card in enumerate(hand.cards):
                if self.stacks.is_playable(card.real_card):
                    yield relative_player_id, slot, card

    @property
    def my_hand(self) -> PlayerHand:
        return self.player_hands[0]

    @property
    def other_player_hands(self) -> tuple[PlayerHand]:
        return self.player_hands[1:]

    def can_give_clue(self):
        return self.clue_count > 0

    def can_discard(self):
        return self.clue_count < 8

    def is_possibly_playable(self, card: PlayerCard):
        filtered_possible_cards = set()
        visible_cards = self.visible_cards()
        for possible_card in card.possible_cards:
            if visible_cards.get(possible_card, 0) < possible_card.number_of_copies:
                filtered_possible_cards.add(possible_card)

        return self.stacks.are_all_playable_or_already_played(filtered_possible_cards)

    def visible_cards(self) -> Dict[Card, int]:
        played_cards = {}
        for card in self.stacks.played_cards:
            played_cards[card] = played_cards.get(card, 0) + 1

        for card in self.discard:
            played_cards[card] = played_cards.get(card, 0) + 1

        for hand in self.other_player_hands:
            for card in hand.cards:
                played_cards[card.real_card] = played_cards.get(card.real_card, 0) + 1

        return played_cards


@dataclass(frozen=True)
class GameHistory:
    game_states: List[RelativeGameState] = field(default_factory=list)

    def add_game_state(self, game_state: RelativeGameState) -> None:
        self.game_states.append(game_state)
