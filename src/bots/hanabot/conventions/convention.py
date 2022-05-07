from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterable

from bots.domain.decision import Decision, SuitClueDecision
from bots.domain.model.game_state import RelativeGameState, RelativePlayerNumber, Turn
from bots.domain.model.hand import Hand, HandCard, Slot
from bots.hanabot.blackboard import Interpretation


@dataclass
class Convention(ABC):
    name: str
    document: ConventionDocument = None

    @abstractmethod
    def find_clue(self, card_to_clue: tuple[RelativePlayerNumber, Slot, HandCard], current_game_state: RelativeGameState) -> list[Decision] | None:
        pass

    @abstractmethod
    def find_interpretation(self, turn: Turn) -> Interpretation | None:
        pass


@dataclass(frozen=True)
class ConventionDocument:
    play_conventions: list[Convention] = field(default_factory=list)
    save_conventions: list[Convention] = field(default_factory=list)

    def __post_init__(self):
        for convention in self.play_conventions:
            convention.document = self
        for convention in self.save_conventions:
            convention.document = self

    def find_save(self, critical_card: tuple[RelativePlayerNumber, Slot, HandCard], current_game_state: RelativeGameState) -> list[Decision]:
        for convention in self.save_conventions:
            decisions = convention.find_clue(critical_card, current_game_state)
            if decisions is not None:
                return decisions
        return []

    def find_chop(self, hand: Hand) -> int | None:
        return next((slot for slot, card in list(enumerate(hand))[::-1] if not card.is_clued), None)

    def find_card_on_chop(self, player_hand: Hand) -> HandCard | None:
        chop = self.find_chop(player_hand)
        if chop is None:
            return None

        return player_hand[self.find_chop(player_hand)]

    def find_play_clue(
        self,
        playable_cards: Iterable[tuple[RelativePlayerNumber, Slot, HandCard]] | tuple[RelativePlayerNumber, Slot, HandCard],
        current_game_state: RelativeGameState,
    ) -> Iterable[Decision]:
        if isinstance(playable_cards, tuple):
            playable_cards = [playable_cards]

        possible_decisions = []
        for playable_card in playable_cards:
            for convention in self.play_conventions:
                decisions = convention.find_clue(playable_card, current_game_state)
                if decisions is not None:
                    possible_decisions.extend(decisions)

        return possible_decisions

    def find_stall(self, current_game_state: RelativeGameState) -> list[Decision]:
        for relative_player_id, hand in enumerate(current_game_state.other_player_hands, 1):
            for card in hand:
                if card.is_clued:
                    return [SuitClueDecision(card.real_card.suit, relative_player_id)]
        return [SuitClueDecision(current_game_state.other_player_hands[0][0].real_card.suit, 1)]

    def find_new_interpretations(self, turn: Turn) -> list[Interpretation]:
        interpretations = []
        for convention in self.save_conventions + self.play_conventions:
            # TODO should probably pass the game state at the time the clue was given
            interpretation = convention.find_interpretation(turn)
            if interpretation is not None:
                interpretations.append(interpretation)

        return interpretations
