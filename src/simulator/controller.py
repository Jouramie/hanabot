import logging
import os
from datetime import datetime
from typing import List, Dict, Iterable

from core import Deck, Suit
from simulator.game.game import Game
from simulator.game.gameresult import GameResult
from core.state.gamestate import GameState
from simulator.game.player import Player
from simulator.players.simulatorplayer import SimulatorPlayer

logger = logging.getLogger(__name__)

CURRENT_GAME_FILE = "logs/current_game.txt"
PAST_GAMES_FOLDER = "logs/past_games"
MAX_LOGGED_GAMES = 100


class Controller:
    current_game: Game
    current_players: Dict[str, SimulatorPlayer]

    def __init__(self, verbose=True, log_game=True):
        self.draw_game_enabled = verbose
        self.log_game_enabled = log_game
        self.current_game_file = None

    def new_game(self, players: List[SimulatorPlayer], suits: Iterable[Suit]) -> Game:
        self.current_game = Game([player.name for player in players], Deck.generate(suits))
        self._initialize_players(players)
        if self.log_game_enabled:
            if os.path.isfile(CURRENT_GAME_FILE):
                os.remove(CURRENT_GAME_FILE)
            self.current_game_file = open(CURRENT_GAME_FILE, "w+")
        return self.current_game

    def resume_game(self, players: List[SimulatorPlayer], game: Game) -> Game:
        self.current_game = game
        self._initialize_players(players)
        return self.current_game

    def _initialize_players(self, players: List[SimulatorPlayer]):
        self.current_players = {}
        for player in players:
            player.new_game()
            self.current_players[player.name] = player

    def play_turn(self) -> GameState:
        player_to_play_name = self.current_game.players[self.current_game.player_turn].name
        player_to_play = self.current_players[player_to_play_name]
        action = player_to_play.play_turn(self.current_game)
        self.current_game.play_turn(action)
        return self.current_game

    def try_play_until_game_is_over(self):
        result = None
        try:
            result = self.play_until_game_is_over()
            return result
        except Exception as e:
            logger.exception(e)
            self.current_game.status.is_over = True
            self.current_game.status.strikes = 3
            result = GameResult.from_game_state(self.current_game)
            return result
        finally:
            self.draw_and_log(repr(result))
            if self.current_game_file is not None:
                self.close_game_log(result.score)

    def play_until_game_is_over(self) -> GameResult:
        while not self.is_game_over():
            self.play_turn()
            self.draw_game()
        return self.get_game_result()

    def is_game_over(self) -> bool:
        return self.current_game.status.is_over

    def get_game_result(self) -> GameResult:
        return GameResult.from_game_state(self.current_game)

    def draw_game(self):
        self.draw_last_action()
        self.draw_game_numbers()
        self.draw_stacks()
        self.draw_hands()
        self.draw_and_log("-------------------------------")

    def draw_last_action(self):
        if self.current_game.history.actions:
            self.draw_and_log(f"{self.current_game.history.actions[-1]}")

    def draw_game_numbers(self):
        clues = str(self.current_game.status.clues)
        strikes = str(self.current_game.status.strikes)
        deck = str(self.current_game.deck.number_cards())
        score = 0
        for stack in self.current_game.play_area.stacks.values():
            score = score + stack.stack_score()
        score = str(score)
        turns = str(self.current_game.status.turns_remaining)
        self.draw_and_log("Clues: " + clues + " | Strikes: " + strikes + " | Score: " + score + " | Turns: " + turns + " | Deck: " + deck)

    def draw_stacks(self):
        stack_string = "Stacks: | "
        for suit, stack in self.current_game.play_area.stacks.items():
            stack_string += str(stack) + " | "
        self.draw_and_log(stack_string)

    def draw_hands(self):
        self.draw_and_log("")
        for player in self.current_game.players:
            self.draw_hand(player)

    def draw_hand(self, player: Player):
        hand_string = f"{str(player) + ':' :{' '}<{8}}" + " |"
        for card in player.hand:
            if card.is_clued:
                hand_string += f"[{str(card)}]|"
            else:
                hand_string += f" {str(card)} |"
        self.draw_and_log(hand_string)

    def draw_and_log(self, string: str):
        if self.draw_game_enabled:
            print(string)
        if self.log_game_enabled:
            self.current_game_file.write(string + "\n")

    def close_game_log(self, score: int | None):
        self.current_game_file.close()
        if not os.path.isdir(PAST_GAMES_FOLDER):
            os.mkdir(PAST_GAMES_FOLDER)
        if score is not None:
            file_destination = f"{PAST_GAMES_FOLDER}/{datetime.now().replace().isoformat().replace(':', '')}-{str(score)}.txt"
        else:
            file_destination = f"{PAST_GAMES_FOLDER}/{datetime.now().replace().isoformat().replace(':', '')}.txt"
        os.rename(CURRENT_GAME_FILE, file_destination)
        saved_games = os.listdir(PAST_GAMES_FOLDER)
        if len(saved_games) > MAX_LOGGED_GAMES:
            os.remove(f"{PAST_GAMES_FOLDER}/{sorted(saved_games)[0]}")
