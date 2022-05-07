from frozendict import frozendict

from bots.domain.decision import DecisionMaking, Decision, PlayDecision, DiscardDecision, SuitClueDecision, RankClueDecision
from bots.domain.model.action import Action, PlayAction, DiscardAction, SuitClueAction, RankClueAction
from bots.domain.model.game_state import RelativeGameState, GameHistory, Turn
from bots.domain.model.hand import Hand, HandCard
from bots.domain.model.stack import Stacks, Stack
from core import Suit, Card
from core.discard import Discard
from core.state.discard_pile import DiscardPile
from core.state.gamestate import GameState as SimulatorGameState
from core.state.stack import Stack as SimulatorStack
from simulator.game.action import (
    Action as SimulatorAction,
    PlayAction as SimulatorPlayAction,
    DiscardAction as SimulatorDiscardAction,
    ColorClueAction as SimulatorColorClueAction,
    RankClueAction as SimulatorRankClueAction,
)
from simulator.game.clue import Clue as SimulatorClue
from simulator.game.game import Game
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
        tuple(HandCard(frozenset(hand_card.possible_cards), hand_card.is_clued, hand_card.draw_id, hand_card.real_card) for hand_card in player.hand),
    )


def assemble_player_hands(game_state: SimulatorGameState) -> tuple[Hand, ...]:
    hands = []

    for player in game_state.players:
        if player == game_state.current_player:
            hands.append(assemble_my_hand(player))
        else:
            hands.append(assemble_other_player_hands(player))

    return tuple(hands[game_state.player_turn :] + hands[: game_state.player_turn])


def assemble_action(action: SimulatorAction | None, clue: SimulatorClue | None) -> Action:
    if action is None:
        return None

    if isinstance(action, SimulatorPlayAction):
        return PlayAction(action.drawId, action.playedCard)
    if isinstance(action, SimulatorDiscardAction):
        return DiscardAction(action.drawId, action.discardedCard)
    if isinstance(action, SimulatorColorClueAction):
        return SuitClueAction(action.target_player.name, frozenset(clue.touched_slots), frozenset(clue.touched_draw_ids), action.color)
    if isinstance(action, SimulatorRankClueAction):
        return RankClueAction(action.target_player.name, frozenset(clue.touched_slots), frozenset(clue.touched_draw_ids), action.rank)
    raise ValueError(f"Unknown action: {action}")


def assemble_simulator_decision(decision: Decision, game: Game) -> SimulatorAction:
    if isinstance(decision, PlayDecision):
        return SimulatorPlayAction(decision.slot)
    if isinstance(decision, DiscardDecision):
        return SimulatorDiscardAction(decision.slot)
    if isinstance(decision, SuitClueDecision):
        return SimulatorColorClueAction(decision.suit, game.get_relative_player(decision.receiver))
    if isinstance(decision, RankClueDecision):
        return SimulatorRankClueAction(decision.rank, game.get_relative_player(decision.receiver))

    raise ValueError(f"Unknown decision: {decision}")


def add_recent_turns_to_history(history: GameHistory, game: Game) -> GameHistory:
    if game.history.gamestates:
        last_turn_in_history = history.turns[-1].game_state.turn_number if history.turns else 0
        for action, game_state in zip(game.history.actions[last_turn_in_history:], game.history.gamestates[last_turn_in_history:]):
            # TODO see if reversing the clue list optimises the performance
            clue = next((clue for clue in game.history.clues if clue.turn == action.turn), None)
            history.add_game_state(Turn(assemble_relative_game_state(game_state), assemble_action(action, clue)))

    return history


def assemble_discard(discard_pile: DiscardPile) -> Discard:
    discard: dict[Card, int] = {}
    for card in discard_pile.cards:
        discard[card] = discard.get(card, 0) + 1

    return Discard(frozendict(discard))


def assemble_relative_game_state(game_state: SimulatorGameState) -> RelativeGameState:
    return RelativeGameState(
        assemble_stacks(game_state.play_area.stacks),
        assemble_discard(game_state.discard_pile),
        assemble_player_hands(game_state),
        game_state.status.turn,
        game_state.status.clues,
        game_state.status.strikes,
    )


class SimulatorBot(SimulatorPlayer):
    def __init__(self, name: str, decision_making: DecisionMaking):
        super().__init__(name)
        self.decision_making = decision_making
        self.history = None

    def new_game(self):
        self.decision_making.new_game()
        self.history = GameHistory()

    def play_turn(self, game: Game) -> SimulatorAction:
        add_recent_turns_to_history(self.history, game)
        current_game_state = assemble_relative_game_state(game.current_state)

        decision = self.decision_making.play_turn(current_game_state, self.history)

        return assemble_simulator_decision(decision, game)
