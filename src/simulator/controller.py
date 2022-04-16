from typing import List, Dict

from simulator.game.card import Suit
from simulator.game.gameresult import GameResult
from simulator.game.gamestate import GameState
from simulator.players.simulatorplayer import SimulatorPlayer


class Controller:
    current_game: GameState
    current_players: Dict[str, SimulatorPlayer]

    def new_game(self, players: List[SimulatorPlayer], suits: List[Suit]) -> GameState:
        self.current_game = GameState([player.get_name() for player in players], suits)
        self.current_players = {}
        for player in players:
            self.current_players[player.get_name()] = player

    def play_turn(self) -> GameState:
        player_to_play_name = self.current_game.players[self.current_game.playerTurn].name
        player_to_play = self.current_players[player_to_play_name]
        action = player_to_play.play_turn(self.current_game)
        self.current_game.play_turn(action)
        return self.current_game

    def play_until_game_is_over(self) -> GameResult:
        while not self.is_game_over():
            self.play_turn()
        return self.get_game_result()

    def is_game_over(self) -> bool:
        return self.current_game.isOver

    def get_game_result(self) -> GameResult:
        return GameResult(self.current_game)
