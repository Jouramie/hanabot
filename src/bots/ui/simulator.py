from bots.domain.decision import DecisionMaking, Decision, PlayDecision, DiscardDecision, SuitClueDecision, RankClueDecision
from bots.domain.model.action import Action, PlayAction, DiscardAction, ClueAction
from bots.domain.model.clue import SuitClue, RankClue
from bots.domain.model.game_state import RelativeGameState, GameHistory
from bots.domain.model.stack import Stacks, Stack
from core import Suit
from simulator.game.action import (
    Action as SimulatorAction,
    PlayAction as SimulatorPlayAction,
    DiscardAction as SimulatorDiscardAction,
    ClueAction as SimulatorClueAction,
)
from simulator.game.clue import ColorClue as SimulatorColorClue, RankClue as SimulatorRankClue
from simulator.game.gamestate import GameState as GlobalGameState
from simulator.game.stack import Stack as SimulatorStack
from simulator.players.simulatorplayer import SimulatorPlayer


def assemble_stacks(stacks: dict[Suit, SimulatorStack]) -> Stacks:
    return Stacks({suit: Stack(stack.suit, stack.last_played) for suit, stack in stacks.items()})


def assemble_last_performed_action(history: list[SimulatorAction]) -> Action | None:
    if not history:
        return None

    action = history[-1]

    if isinstance(action, SimulatorPlayAction):
        return PlayAction(action.playedCard)
    if isinstance(action, SimulatorDiscardAction):
        return DiscardAction(action.discardedCard)
    if isinstance(action, SimulatorClueAction):
        if isinstance(action.clue, SimulatorColorClue):
            return ClueAction(action.clue.receiver.name, SuitClue(set(), action.clue.suit))  # TODO
        if isinstance(action.clue, SimulatorRankClue):
            return ClueAction(action.clue.receiver.name, RankClue(set(), action.clue.rank))  # TODO
    return None


def assemble_simulator_decision(decision: Decision, global_state: GlobalGameState) -> SimulatorAction:
    if isinstance(decision, PlayDecision):
        return SimulatorPlayAction(decision.slot)
    if isinstance(decision, DiscardDecision):
        return SimulatorDiscardAction(decision.slot)
    if isinstance(decision, SuitClueDecision):
        return SimulatorClueAction(
            SimulatorColorClue(decision.suit, global_state.players[(global_state.player_turn + decision.receiver + 1) % len(global_state.players)])
        )
    if isinstance(decision, RankClueDecision):
        return SimulatorClueAction(
            SimulatorRankClue(decision.rank, global_state.players[(global_state.player_turn + decision.receiver + 1) % len(global_state.players)])
        )
    raise ValueError(f"Unknown decision: {decision}")


class SimulatorBot(SimulatorPlayer):
    def __init__(self, name: str, decision_making: DecisionMaking):
        super().__init__(name)
        self.decision_making = decision_making

    def play_turn(self, global_game_state: GlobalGameState) -> SimulatorAction:
        relative_game_state = RelativeGameState(
            assemble_stacks(global_game_state.stacks),
            tuple(global_game_state.discard_pile),
            None,  # TODO
            None,  # TODO
            assemble_last_performed_action(global_game_state.action_history),
            global_game_state.current_turn,
            global_game_state.current_clues,
            global_game_state.current_strikes,
        )

        decision = self.decision_making.play_turn(relative_game_state, GameHistory())

        return assemble_simulator_decision(decision, global_game_state)
