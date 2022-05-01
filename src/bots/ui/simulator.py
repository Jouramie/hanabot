from bots.domain.decision import DecisionMaking, Decision, PlayDecision, DiscardDecision, SuitClueDecision, RankClueDecision
from bots.domain.model.action import Action, PlayAction, DiscardAction, SuitClueAction, RankClueAction
from bots.domain.model.game_state import RelativeGameState, GameHistory
from bots.domain.model.hand import Hand, HandCard
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
from simulator.game.clue import Clue as SimulatorClue
from simulator.game.gamestate import GameState as GlobalGameState
from simulator.game.history import History as SimulatorHistory
from simulator.game.player import Player
from simulator.players.simulatorplayer import SimulatorPlayer


def assemble_stacks(stacks: dict[Suit, SimulatorStack]) -> Stacks:
    return Stacks({suit: Stack(stack.suit, stack.last_played) for suit, stack in stacks.items()})


def assemble_my_hand(me: Player) -> Hand:
    # TODO add drawn turn
    return Hand(me.name, tuple(HandCard(frozenset(hand_card.possible_cards), hand_card.is_clued, hand_card.draw_id) for hand_card in me.hand))


def assemble_other_player_hands(player: Player) -> Hand:
    return Hand(
        player.name,
        tuple(
            HandCard(frozenset(hand_card.possible_cards), len(hand_card.received_clues) > 0, hand_card.draw_id, hand_card.real_card)
            for hand_card in player.hand
        ),
    )


def assemble_player_hands(global_state: GlobalGameState) -> tuple[Hand, ...]:
    hands = []

    for player in global_state.players:
        if player == global_state.current_player:
            hands.append(assemble_my_hand(player))
        else:
            hands.append(assemble_other_player_hands(player))

    return tuple(hands[global_state.player_turn :] + hands[: global_state.player_turn])


def assemble_action(action: SimulatorAction, clues: list[SimulatorClue]) -> Action:
    if isinstance(action, SimulatorPlayAction):
        return PlayAction(action.drawId, action.playedCard)
    if isinstance(action, SimulatorDiscardAction):
        return DiscardAction(action.drawId, action.discardedCard)
    if isinstance(action, SimulatorColorClueAction):
        clue = next(clue for clue in clues if clue.turn == action.turn)
        return SuitClueAction(action.target_player.name, frozenset(clue.touched_slots), action.color)
    if isinstance(action, SimulatorRankClueAction):
        clue = next(clue for clue in clues if clue.turn == action.turn)
        return RankClueAction(action.target_player.name, frozenset(clue.touched_slots), action.rank)
    return None


def assemble_last_performed_action(history: SimulatorHistory) -> Action | None:
    if not history.actions:
        return None
    action = history.actions[-1]
    return assemble_action(action, history.clues)


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


def assemble_history(global_game_state: GlobalGameState) -> GameHistory:
    history = GameHistory()

    for action in global_game_state.history.actions:
        # FIXME bruh
        history.add_game_state(RelativeGameState(None, None, None, assemble_action(action, global_game_state.history.clues), None, None, None))

    return history


def assemble_relative_gamestate(global_gamestate: GlobalGameState) -> RelativeGameState:
    return RelativeGameState(
            assemble_stacks(global_gamestate.play_area.stacks),
            tuple(global_gamestate.discard_pile.cards),
            assemble_player_hands(global_gamestate),
            assemble_last_performed_action(global_gamestate.history),
            global_gamestate.status.turn,
            global_gamestate.status.clues,
            global_gamestate.status.strikes,
        )


class SimulatorBot(SimulatorPlayer):
    def __init__(self, name: str, decision_making: DecisionMaking):
        super().__init__(name)
        self.decision_making = decision_making

    def play_turn(self, global_game_state: GlobalGameState) -> SimulatorAction:
        relative_game_state = assemble_relative_gamestate(global_game_state)

        history = assemble_history(global_game_state)

        decision = self.decision_making.play_turn(relative_game_state, history)

        return assemble_simulator_decision(decision, global_game_state)
