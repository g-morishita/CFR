import numpy as np
import game

class Player():
    """
    Player class that has a normal game info.
    """
    def __init__(self, normal_game, player):
        if isinstance(normal_game, game.OneshotGame):
            raise TypeError(f"OneShotGame instance is only acceptable. Your input's type is {type(normal_game)}")

        if player > normal_game.num_players:
            raise game.ExceedNumPlayersError(f"Your input player exceeds the number of players in the given game. The limit is {normal_game.num_players}, but your input is {player}")

        self.normal_game = normal_game
        self.player = player
        self.num_actions = self.normal_game.num_strategies[self.player]
        self.regret_sum = np.zero(self.num_actions)
