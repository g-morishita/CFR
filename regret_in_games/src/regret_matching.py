import numpy as np
import normal_game

class Player():
    """
    Player class that has a normal game info.
    """
    # the game the player play
    game = normal_game.OneShotGame()

    def __init__(self, player, game = None):
        # If a game to play is set, initialize.
        if game is not None:
            self.init_game(game)
            self.initilize_player(player)
        else:
            self.player = player
            self.num_actions = 0
            self.regret_sum = None



    def initilize_player(self, player):
        if player > self.game.num_players:
            raise normal_game.ExceedNumPlayersError(f"Your input player exceeds the number of players in the given game. "
                                                    f"The limit is {self.game.num_players}, but your input is {player}")

        self.player = player
        self.num_actions = self.game.num_strategies[self.player]
        self.regret_sum = np.zero(self.num_actions)


    def init_game(self, game_matrix):
        """initiate the normal game"""
        self.game.initilize_game(game_matrix)
        self.initilize_player(self.player)


    def simulate_game(self, other_players):
        """
        simulate the game and return the regret in the simulated game
        :return: regret (np.ndarray)
        """
        # check if other players are actually players
        if not np.array([isinstance(player, self) for player in other_players]).all():
            raise NotPlayerError("The inputs are inavlid. The acceptable type is only Player.")




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

class NotPlayerError(Exception):
    def __init__(self, message):
        self.message = message
