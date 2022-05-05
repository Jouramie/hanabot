from frozendict import frozendict

from bots.domain.decision import DecisionMaking, Decision, PlayDecision, DiscardDecision, SuitClueDecision, RankClueDecision
from bots.domain.model.action import Action, PlayAction, DiscardAction, SuitClueAction, RankClueAction
from bots.domain.model.game_state import RelativeGameState, GameHistory
from bots.domain.model.hand import Hand, HandCard
from bots.domain.model.stack import Stacks, Stack
from core import Suit, Card
from core.discard import Discard
from core.state.discard_pile import DiscardPile
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
        tuple(HandCard(frozenset(hand_card.possible_cards), hand_card.is_clued, hand_card.draw_id, hand_card.real_card) for hand_card in player.hand),
    )


def assemble_player_hands(game: Game) -> tuple[Hand, ...]:
    hands = []

    for player in game.players:
        if player == game.current_player:
            hands.append(assemble_my_hand(player))
        else:
            hands.append(assemble_other_player_hands(player))

    return tuple(hands[game.player_turn :] + hands[: game.player_turn])


def assemble_action(action: SimulatorAction, clues: list[SimulatorClue]) -> Action:
    if isinstance(action, SimulatorPlayAction):
        return PlayAction(action.drawId, action.playedCard)
    if isinstance(action, SimulatorDiscardAction):
        return DiscardAction(action.drawId, action.discardedCard)
    if isinstance(action, SimulatorColorClueAction):
        clue = next(clue for clue in clues if clue.turn == action.turn)
        return SuitClueAction(action.target_player.name, frozenset(clue.touched_slots), frozenset(clue.touched_draw_ids), action.color)
    if isinstance(action, SimulatorRankClueAction):
        clue = next(clue for clue in clues if clue.turn == action.turn)
        return RankClueAction(action.target_player.name, frozenset(clue.touched_slots), frozenset(clue.touched_draw_ids), action.rank)
    return None


def assemble_last_performed_action(history: SimulatorHistory) -> Action | None:
    if not history.actions:
        return None
    action = history.actions[-1]
    return assemble_action(action, history.clues)


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


def assemble_history(game: Game) -> GameHistory:
    history = GameHistory()

    for action in game.history.actions:
        # FIXME bruh
        history.add_game_state(RelativeGameState(None, None, None, assemble_action(action, game.history.clues), None, None, None))

    return history


def assemble_discard(discard_pile: DiscardPile) -> Discard:
    discard: dict[Card, int] = {}
    for card in discard_pile.cards:
        discard[card] = discard.get(card, 0) + 1

    return Discard(frozendict(discard))


def assemble_relative_gamestate(game: Game) -> RelativeGameState:
    return RelativeGameState(
        assemble_stacks(game.play_area.stacks),
        assemble_discard(game.discard_pile),
        assemble_player_hands(game),
        assemble_last_performed_action(game.history),
        game.status.turn,
        game.status.clues,
        game.status.strikes,
    )


class SimulatorBot(SimulatorPlayer):
    def __init__(self, name: str, decision_making: DecisionMaking):
        super().__init__(name)
        self.decision_making = decision_making

    def new_game(self):
        self.decision_making.new_game()

    def play_turn(self, game: Game) -> SimulatorAction:
        relative_game_state = assemble_relative_gamestate(game)

        history = assemble_history(game)

        decision = self.decision_making.play_turn(relative_game_state, history)

        return assemble_simulator_decision(decision, game)
