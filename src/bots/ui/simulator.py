from bots.domain.decision import DecisionMaking, Decision, PlayDecision, DiscardDecision, SuitClueDecision, RankClueDecision
from bots.domain.model.action import Action, PlayAction, DiscardAction, SuitClueAction, RankClueAction
from bots.domain.model.game_state import RelativeGameState, GameHistory, Turn
from bots.domain.model.hand import Hand, HandCard, DrawId
from core.state.gamestate import GameState as SimulatorGameState
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


def assemble_my_hand(me: Player, hand_card_cache: dict[DrawId, HandCard]) -> Hand:
    cards = []
    for hand_card in me.hand:
        if hand_card.draw_id in hand_card_cache:
            cards.append(hand_card_cache[hand_card.draw_id])
        else:
            cards.append(HandCard(frozenset(hand_card.possible_cards), hand_card.is_clued, hand_card.draw_id))
            hand_card_cache[hand_card.draw_id] = cards[-1]

    return Hand(me.name, tuple(cards))


def assemble_other_player_hands(player: Player, hand_card_cache: dict[DrawId, HandCard]) -> Hand:
    cards = []
    for hand_card in player.hand:
        if hand_card.draw_id in hand_card_cache:
            cards.append(hand_card_cache[hand_card.draw_id])
        else:
            cards.append(HandCard(frozenset(hand_card.possible_cards), hand_card.is_clued, hand_card.draw_id, hand_card.real_card))
            hand_card_cache[hand_card.draw_id] = cards[-1]

    return Hand(player.name, tuple(cards))


def assemble_player_hands(game_state: SimulatorGameState, from_perspective: str, hand_card_cache: dict[DrawId, HandCard]) -> tuple[Hand, ...]:
    hands = []
    my_hand = None

    for player in game_state.players:
        if player.name == from_perspective:
            my_hand = assemble_my_hand(player, hand_card_cache)
            hands.append(my_hand)
        else:
            hands.append(assemble_other_player_hands(player, hand_card_cache))

    hands.index(my_hand)
    return tuple(hands[hands.index(my_hand) :] + hands[: hands.index(my_hand)])


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


def add_recent_turns_to_history(history: GameHistory, game: Game, from_perspective: str, hand_card_cache: dict[DrawId, HandCard]) -> GameHistory:
    if game.history.gamestates:
        turn_to_add_in_history = history.latest_turn_number + 1 if history.turns else 0
        for action, game_state in zip(game.history.actions[turn_to_add_in_history:], game.history.gamestates[turn_to_add_in_history:]):
            # TODO see if reversing the clue list optimises the performance
            clue = next((clue for clue in game.history.clues if clue.turn == action.turn), None)
            history.add_game_state(Turn(assemble_relative_game_state(game_state, from_perspective, hand_card_cache), assemble_action(action, clue)))

            if clue is not None:
                receiver = next(player for player in game.players if player.name == clue.receiver_name)
                for card in receiver.hand:
                    if card.draw_id in hand_card_cache:
                        hand_card_cache.pop(card.draw_id)

    return history


def assemble_relative_game_state(game_state: SimulatorGameState, from_perspective: str, hand_card_cache: dict[DrawId, HandCard]) -> RelativeGameState:
    return RelativeGameState(
        game_state.play_area,
        game_state.discard_pile,
        assemble_player_hands(game_state, from_perspective, hand_card_cache),
        game_state.status.turn,
        game_state.status.clues,
        game_state.status.strikes,
    )


class SimulatorBot(SimulatorPlayer):
    def __init__(self, name: str, decision_making: DecisionMaking):
        super().__init__(name)
        self.decision_making = decision_making
        self.history = None
        self.hand_card_cache = None

    def new_game(self):
        self.decision_making.new_game()
        self.history = GameHistory()
        self.hand_card_cache = {}

    def play_turn(self, game: Game) -> SimulatorAction:
        current_player = game.current_player.name
        add_recent_turns_to_history(self.history, game, current_player, self.hand_card_cache)
        current_game_state = assemble_relative_game_state(game.current_state, current_player, self.hand_card_cache)

        decision = self.decision_making.play_turn(current_game_state, self.history)

        return assemble_simulator_decision(decision, game)
