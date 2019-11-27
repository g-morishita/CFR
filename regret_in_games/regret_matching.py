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


    def simulate_game(self, other_players):
        """
        simulate the game and return the regret in the simulated game
        :return: regret (np.ndarray)
        """


    def match_regret(self):
        """
        transform the cumulative regret to a mixed strategy
        :return: mixed strategy (np.ndarray)
        """
        # if the cumulative regret is 0, which means that the player hasn't played once, his/her mixed strategy is uniformly random.
        # Note that the initial mixed strategy does not need to be uniformly random.
        if (self.regret_sum == 0).all():
            mixed_strategy = np.tile(1.0 / self.num_actions, self.num_actions)
        else:
            mixed_strategy = self.regret_sum / self.regret_sum.sum()
        return mixed_strategy
