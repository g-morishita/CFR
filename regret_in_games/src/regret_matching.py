import numpy as np
import normal_game
import helper_func

class Player():
    """
    Player class that has a normal game info.
    """
    # the game the player play
    game = normal_game.OneShotGame()

    def __init__(self, player):
        if self.game is not None:
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
        self.regret_sum = np.zeros(self.num_actions)


    def init_game(cls, game_matrix):
        """initiate the normal game"""
        cls.game.initialize_game(game_matrix)


    def simulate_game(self, other_players):
        """
        simulate the game and return the regret in the simulated game
        :return: regret (np.ndarray)
        """
        # check if other players are actually players
        if not np.array([isinstance(player, Player) for player in other_players]).all():
            raise NotPlayerError("The inputs are inavlid. The acceptable type is only Player.")
        other_players = list(other_players)
        all_players = other_players + [self]
        all_players.sort(key=lambda player: player.player)
        mixed_strategies = [player.regret_to_strategy() for player in all_players]
        gained_utilities, played_pure_strategies = self.game.play_prob(mixed_strategies)
        return gained_utilities, played_pure_strategies


    def regret_to_strategy(self):
        """
        transform the cumulative regret to a mixed strategy
        :return: mixed strategy (np.ndarray)
        """
        # if the cumulative regret is 0, his/her mixed strategy is uniformly random.
        # Note that the initial mixed strategy does not need to be uniformly random.
        if (self.regret_sum == 0).all():
            mixed_strategy = np.tile(1.0 / self.num_actions, self.num_actions)
        else:
            mixed_strategy = self.regret_sum / self.regret_sum.sum()
        return mixed_strategy


    def _calc_regrets(self, played_pure_strategies):
        regrets = []
        add_regret = regrets.append
        helper_func.check_list_like(played_pure_strategies)
        base_utility = self.game.play_pure_strategy(played_pure_strategies)[self.player]
        for action in range(self.num_actions):
            played_pure_strategies[self.player] = action
            regret = self.game.play_pure_strategy(played_pure_strategies)[self.player] - base_utility
            add_regret(regret)

        return np.array(regrets)


    def update_cum_regret(self, played_pure_strategies):
        regrets = self._calc_regrets(played_pure_strategies)
        regrets[regrets < 0] = 0
        self.regret_sum += regrets


class NotPlayerError(Exception):
    def __init__(self, message):
        self.message = message
