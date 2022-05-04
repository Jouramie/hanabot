from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterable

from bots.domain.decision import Decision
from bots.domain.model.action import Action
from bots.domain.model.game_state import RelativeGameState, RelativePlayerNumber
from bots.domain.model.hand import Hand, HandCard, Slot
from bots.hanabot.blackboard import Interpretation, Blackboard


@dataclass(frozen=True)
class Convention(ABC):
    name: str

    @abstractmethod
    def find_clue(self, card_to_clue: tuple[RelativePlayerNumber, Slot, HandCard], current_game_state: RelativeGameState) -> list[Decision] | None:
        pass

    @abstractmethod
    def find_interpretation(self, action: Action, current_game_state: RelativeGameState) -> Interpretation | None:
        pass


@dataclass(frozen=True)
class Conventions:
    play_conventions: list[Convention] = field(default_factory=list)
    save_conventions: list[Convention] = field(default_factory=list)

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
        self, playable_cards: Iterable[tuple[RelativePlayerNumber, Slot, HandCard]], current_game_state: RelativeGameState
    ) -> Iterable[Decision]:
        for playable_card in playable_cards:
            for convention in self.play_conventions:
                decisions = convention.find_clue(playable_card, current_game_state)
                if decisions is not None:
                    yield decisions[0]

    def find_new_interpretations(self, action: Action, blackboard: Blackboard) -> list[Interpretation]:
        interpretations = []
        for convention in self.play_conventions + self.save_conventions:
            # TODO should probably pass the game state at the time the clue was given
            interpretation = convention.find_interpretation(action, blackboard.current_game_state)
            if interpretation is not None:
                interpretations.append(interpretation)

        return interpretations
