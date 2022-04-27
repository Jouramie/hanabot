from typing import List, Dict, Iterable

from core import Deck, Suit
from simulator.game.gameresult import GameResult
from simulator.game.gamestate import GameState
from simulator.game.player import Player
from simulator.players.simulatorplayer import SimulatorPlayer


class Controller:
    current_game: GameState
    current_players: Dict[str, SimulatorPlayer]

    def new_game(self, players: List[SimulatorPlayer], suits: Iterable[Suit]) -> GameState:
        self.current_game = GameState([player.name for player in players], Deck.generate(suits))
        self._initialize_players(players)
        return self.current_game

    def resume_game(self, players: List[SimulatorPlayer], game_state: GameState) -> GameState:
        self.current_game = game_state
        self._initialize_players(players)
        return self.current_game

    def _initialize_players(self, players: List[SimulatorPlayer]):
        self.current_players = {}
        for player in players:
            self.current_players[player.name] = player

    def play_turn(self) -> GameState:
        player_to_play_name = self.current_game.players[self.current_game.player_turn].name
        player_to_play = self.current_players[player_to_play_name]
        action = player_to_play.play_turn(self.current_game)
        self.current_game.play_turn(action)
        return self.current_game

    def play_until_game_is_over(self) -> GameResult:
        while not self.is_game_over():
            self.play_turn()
            self.draw_game()
        return self.get_game_result()

    def is_game_over(self) -> bool:
        return self.current_game.status.is_over

    def get_game_result(self) -> GameResult:
        return GameResult(self.current_game)

    def draw_game(self):
        self.draw_last_action()
        self.draw_game_numbers()
        self.draw_stacks()
        self.draw_hands()
        print("-------------------------------")

    def draw_last_action(self):
        if self.current_game.history.actions:
            print(str(self.current_game.history.actions[-1]))

    def draw_game_numbers(self):
        clues = str(self.current_game.status.clues)
        strikes = str(self.current_game.status.strikes)
        deck = str(self.current_game.deck.number_cards())
        score = 0
        for stack in self.current_game.play_area.stacks.values():
            score = score + stack.stack_score()
        score = str(score)
        turns = str(self.current_game.status.turns_remaining)
        print("Clues: " + clues + " | Strikes: " + strikes + " | Score: " + score + " | Turns: " + turns + " | Deck: " + deck)

    def draw_stacks(self):
        stack_string = "Stacks: | "
        for suit, stack in self.current_game.play_area.stacks.items():
            stack_string += str(stack) + " | "
        print(stack_string)

    def draw_hands(self):
        print("")
        for player in self.current_game.players:
            self.draw_hand(player)

    def draw_hand(self, player: Player):
        hand_string = f"{str(player) + ':' :{' '}<{8}}" + " |"
        for card in player.hand:
            if card.is_clued:
                hand_string += f"[{str(card)}]|"
            else:
                hand_string += f" {str(card)} |"
        print(hand_string)
