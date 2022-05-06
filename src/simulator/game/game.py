import logging
import random
from copy import deepcopy
from typing import List

from core import Deck
from core.gamerules import get_hand_size
from core.state.discard_pile import DiscardPile
from core.state.gamestate import GameState
from core.state.play_area import PlayArea
from core.state.status import Status
from simulator.game.action import Action, PlayAction, ColorClueAction, RankClueAction, DiscardAction
from simulator.game.clue import ColorClue, RankClue, Clue
from simulator.game.hand_card import HandCard
from simulator.game.history import History
from simulator.game.player import Player

logger = logging.getLogger(__name__)


class Game:
    history: History
    current_state: GameState

    def __init__(self, players_names: List[str], deck: Deck):
        self.history = History()

        deck = deck
        discard_pile = DiscardPile()
        play_area = PlayArea(deck.suits)

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
    def discard_pile(self) -> DiscardPile:
        return self.current_state.discard_pile

    @property
    def play_area(self) -> PlayArea:
        return self.current_state.play_area

    @property
    def status(self) -> Status:
        return self.current_state.status

    def get_relative_player(self, relative_player_id: int) -> Player:
        return self.players[(self.player_turn + relative_player_id) % len(self.players)]

    def player_draw_card(self, player: Player):
        if len(self.deck) == 0:
            return
        draw_id, card = self.deck.draw()
        hand_card = HandCard(draw_id, card, list(self.deck.suits))
        player.hand.insert(0, hand_card)

    def play_turn(self, action: Action):
        self.history.add_state(deepcopy(self.current_state))

        action.actor = self.current_player

        action.act_on_state(self)
        self.status.next_turn()

        action.turn = self.status.turn

        self.history.add_action(action)
        if self.status.turns_remaining == 0:
            self.status.is_over = True

    def play_turn_play(self, action: PlayAction):
        player = self.current_player

        if action.cardSlot < 0 or action.cardSlot >= len(player.hand):
            raise ValueError("You cannot play this slot!")

        card_to_play = player.hand.pop(action.cardSlot)
        stack_to_play_on = self.play_area.stacks[card_to_play.real_card.suit]
        if stack_to_play_on.can_play(card_to_play.real_card):
            stack_to_play_on.play(card_to_play.real_card)
            action.success = True
        else:
            self.status.add_strike()
            self.discard_pile.discard(card_to_play.real_card)
            action.success = False
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
        self.discard_pile.discard(card_to_discard.real_card)
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
