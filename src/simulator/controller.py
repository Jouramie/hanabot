from typing import List, Dict

from simulator.game.card import Suit
from simulator.game.gameresult import GameResult
from simulator.game.gamerules import get_suit_short_name
from simulator.game.gamestate import GameState
from simulator.game.player import Player
from simulator.players.simulatorplayer import SimulatorPlayer


class Controller:
    current_game: GameState
    current_players: Dict[str, SimulatorPlayer]

    def new_game(self, players: List[SimulatorPlayer], suits: List[Suit]) -> GameState:
        self.current_game = GameState([player.get_name() for player in players], suits)
        self.current_players = {}
        for player in players:
            self.current_players[player.get_name()] = player
        return self.current_game

    def play_turn(self) -> GameState:
        player_to_play_name = self.current_game.players[self.current_game.player_turn].name
        player_to_play = self.current_players[player_to_play_name]
        action = player_to_play.play_turn(self.current_game)
        self.current_game.play_turn(action)
        return self.current_game

    def play_until_game_is_over(self) -> GameResult:
        while not self.is_game_over():
            self.play_turn()
        return self.get_game_result()

    def is_game_over(self) -> bool:
        return self.current_game.is_over

    def get_game_result(self) -> GameResult:
        return GameResult(self.current_game)

    def draw_game(self):
        self.draw_stacks()
        self.draw_hands()
        pass

    def draw_stacks(self):
        stack_string = "Stacks: | "
        for suit, stack in self.current_game.stacks.items():
            stack_number = 0
            if stack.last_played is not None:
                stack_number = stack.last_played.number_value
            stack_string += get_suit_short_name(suit) + str(stack_number) + " | "
        print(stack_string)

    def draw_hands(self):
        print("")
        for player in self.current_game.players:
            self.draw_hand(player)

    def draw_hand(self, player: Player):
        hand_string = player.name + ": | "
        for card in player.hand:
            hand_string += get_suit_short_name(card.suit) + str(card.number_value) + " | "
        print(hand_string)
