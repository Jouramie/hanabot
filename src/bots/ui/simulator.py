from bots.domain.decision import DecisionMaking, Decision, PlayDecision, DiscardDecision, SuitClueDecision, RankClueDecision
from bots.domain.model.action import Action, PlayAction, DiscardAction, ClueAction
from bots.domain.model.clue import SuitClue, RankClue
from bots.domain.model.game_state import RelativeGameState, GameHistory
from bots.domain.model.player import PlayerHand, PlayerCard
from bots.domain.model.stack import Stacks, Stack
from core import Suit
from core.state.stack import Stack as SimulatorStack
from simulator.game.action import (
    Action as SimulatorAction,
    PlayAction as SimulatorPlayAction,
    DiscardAction as SimulatorDiscardAction,
    ColorClueAction as SimulatorColorClueAction,
    RankClueAction as SimulatorRankClueAction,
)
from simulator.game.gamestate import GameState as GlobalGameState
from simulator.game.history import History as SimulatorHistory
from simulator.game.player import Player
from simulator.players.simulatorplayer import SimulatorPlayer


def assemble_stacks(stacks: dict[Suit, SimulatorStack]) -> Stacks:
    return Stacks({suit: Stack(stack.suit, stack.last_played) for suit, stack in stacks.items()})


def assemble_my_hand(me: Player) -> PlayerHand:
    # TODO add drawn turn
    return PlayerHand(me.name, tuple(PlayerCard(hand_card.possible_cards, hand_card.is_clued, None) for hand_card in me.hand))


def assemble_other_player_hands(player: Player) -> PlayerHand:
    return PlayerHand(
        player.name, tuple(PlayerCard(hand_card.possible_cards, len(hand_card.received_clues) > 0, None, hand_card.real_card) for hand_card in player.hand)
    )


def assemble_player_hands(global_state: GlobalGameState) -> tuple[PlayerHand, ...]:
    hands = []

    for player in global_state.players:
        if player == global_state.current_player:
            hands.append(assemble_my_hand(player))
        else:
            hands.append(assemble_other_player_hands(player))

    return tuple(hands[global_state.player_turn :] + hands[: global_state.player_turn])


def assemble_last_performed_action(history: SimulatorHistory) -> Action | None:
    if not history.actions:
        return None

    action = history.actions[-1]

    if isinstance(action, SimulatorPlayAction):
        return PlayAction(action.playedCard)
    if isinstance(action, SimulatorDiscardAction):
        return DiscardAction(action.discardedCard)
    if isinstance(action, SimulatorColorClueAction):
        return ClueAction(action.target_player.name, SuitClue(set(), action.color))  # TODO
    if isinstance(action, SimulatorRankClueAction):
        return ClueAction(action.target_player.name, RankClue(set(), action.rank))  # TODO
    return None


def assemble_simulator_decision(decision: Decision, global_state: GlobalGameState) -> SimulatorAction:
    if isinstance(decision, PlayDecision):
        return SimulatorPlayAction(decision.slot)
    if isinstance(decision, DiscardDecision):
        return SimulatorDiscardAction(decision.slot)
    if isinstance(decision, SuitClueDecision):
        return SimulatorColorClueAction(decision.suit, global_state.get_relative_player(decision.receiver))
    if isinstance(decision, RankClueDecision):
        return SimulatorRankClueAction(decision.rank, global_state.get_relative_player(decision.receiver))

    raise ValueError(f"Unknown decision: {decision}")


class SimulatorBot(SimulatorPlayer):
    def __init__(self, name: str, decision_making: DecisionMaking):
        super().__init__(name)
        self.decision_making = decision_making

    def play_turn(self, global_game_state: GlobalGameState) -> SimulatorAction:
        relative_game_state = RelativeGameState(
            assemble_stacks(global_game_state.play_area.stacks),
            tuple(global_game_state.discard_pile.cards),
            assemble_player_hands(global_game_state),
            assemble_last_performed_action(global_game_state.history),
            global_game_state.status.turn,
            global_game_state.status.clues,
            global_game_state.status.strikes,
        )

        decision = self.decision_making.play_turn(relative_game_state, GameHistory())

        return assemble_simulator_decision(decision, global_game_state)
