import logging
import random
from copy import deepcopy
from typing import List

from core import Deck, Rank
from core.discard import Discard
from core.gamerules import get_hand_size
from core.stack import Stacks
from core.state.gamestate import GameState
from core.state.status import Status
from simulator.game.action import Action, PlayAction, ColorClueAction, RankClueAction, DiscardAction
from simulator.game.clue import ColorClue, RankClue, Clue
from simulator.game.hand_card import HandCard
from simulator.game.history import History
from simulator.game.player import Player
from util.profiling import timeit

logger = logging.getLogger(__name__)


class Game:
    history: History
    current_state: GameState

    def __init__(self, players_names: List[str], deck: Deck):
        self.history = History()

        deck = deck
        discard_pile = Discard()
        play_area = Stacks.create_empty_stacks(deck.suits)

        players = []
        for playerName in players_names:
            players.append(Player(playerName))
        random.shuffle(players)
        number_of_players = len(players)

        number_cards_in_hands = get_hand_size(number_of_players) * number_of_players

        status = Status(number_of_players + deck.number_cards() - number_cards_in_hands)
        self.current_state = GameState(players, deck, discard_pile, play_area, status)

        for i in range(0, number_cards_in_hands):
            player_index = i % number_of_players
            self.player_draw_card(self.players[player_index])

    @property
    def player_turn(self) -> int:
        return self.status.turn % len(self.players)

    @property
    def players(self) -> List[Player]:
        return self.current_state.players

    @property
    def deck(self) -> Deck:
        return self.current_state.deck

    @property
    def status(self) -> Status:
        return self.current_state.status

    def get_relative_player(self, relative_player_id: int) -> Player:
        return self.players[(self.player_turn + relative_player_id) % len(self.players)]

    def player_draw_card(self, player: Player):
        if len(self.deck) == 0:
            return
        draw_id, card = self.deck.draw()
        hand_card = HandCard(draw_id, card, self.deck.suits)
        player.hand.insert(0, hand_card)

    @timeit(name="Simulator.play_turn")
    def play_turn(self, action: Action):
        self.history.add_state(deepcopy(self.current_state))

        action.actor = self.current_player

        action.act_on_state(self)
        self.status.next_turn()

        action.turn = self.status.turn

        self.history.add_action(action)
        if self.status.turns_remaining == 0 or not self.can_still_get_points(self.status.turns_remaining):
            self.status.is_over = True

    def play_turn_play(self, action: PlayAction):
        player = self.current_player

        if action.cardSlot < 0 or action.cardSlot >= len(player.hand):
            raise ValueError("You cannot play this slot!")

        card_to_play = player.hand.pop(action.cardSlot)

        self.current_state, action.success = self.current_state.play(card_to_play.real_card)

        if action.success:
            if card_to_play.real_card.rank == Rank.FIVE and self.status.clues < 8:
                self.status.clues += 1
        else:
            self.status.add_strike()
            self.current_state = self.current_state.discard(card_to_play.real_card)

        self.player_draw_card(player)
        action.playedCard = card_to_play
        action.drawId = card_to_play.draw_id
        self.status.turns_remaining -= 1

    def play_turn_color_clue(self, action: ColorClueAction):
        suit_is_in_game = False
        for suit in self.deck.suits:
            if suit == action.color:
                suit_is_in_game = True

        if not suit_is_in_game:
            raise ValueError("You cannot clue a suit that is not in the game!")

        clue = ColorClue(action.color, action.target_player.name, self.current_player.name, self.status.turn + 1)
        self.play_turn_clue(clue, action.target_player)

    def play_turn_rank_clue(self, action: RankClueAction):
        clue = RankClue(action.rank, action.target_player.name, self.current_player.name, self.status.turn + 1)
        self.play_turn_clue(clue, action.target_player)

    def play_turn_clue(self, clue: Clue, target_player: Player):

        if target_player == self.current_player:
            raise ValueError("You cannot clue yourself!")

        if self.players.count(target_player) < 1:
            raise ValueError("You cannot clue someone outside of the game!")

        self.status.consume_clue()

        touches_any = False

        for slot, hand_card in enumerate(target_player.hand):
            touched_the_card = hand_card.receive_clue(clue)
            if touched_the_card:
                clue.touched_slots.add(slot)
                clue.touched_draw_ids.add(hand_card.draw_id)
            touches_any |= touched_the_card

        if not touches_any:
            raise ValueError("Empty clues are not allowed in this game!")

        self.history.add_clue(clue)
        if self.deck.is_empty():
            self.status.turns_remaining -= 1

    def play_turn_discard(self, action: DiscardAction):
        player = self.current_player

        if self.status.clues >= 8:
            raise ValueError("You cannot discard at 8 clues!")
        if action.cardSlot is None or action.cardSlot < 0 or action.cardSlot >= len(player.hand):
            raise ValueError("You cannot discard this slot!")

        card_to_discard = player.hand.pop(action.cardSlot)
        self.current_state = self.current_state.discard(card_to_discard.real_card)
        self.status.generate_clue()
        self.player_draw_card(player)
        action.discardedCard = card_to_discard.real_card
        action.drawId = card_to_discard.draw_id
        self.status.turns_remaining -= 1

    @property
    def current_player(self):
        return self.players[self.player_turn]

    def get_player_by_name(self, name: str):
        for player in self.players:
            if player.name == name:
                return player

    def can_still_get_points(self, turns_remaining: int) -> bool:
        for deck_card in self.deck:
            if self.current_state.play_area.can_play(deck_card):
                return True
        for i in range(0, min(turns_remaining, len(self.players))):
            player_index = (self.player_turn + i) % len(self.players)
            player = self.players[player_index]
            for hand_card in player.hand:
                if self.current_state.play_area.can_play(hand_card.real_card):
                    return True
        return False
