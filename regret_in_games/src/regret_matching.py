import numpy as np
import normal_game
import helper_func

class Player():
    """
    Class that has player information.

    Parameters
    ----------
    player : int
        The player in the game.

    strategy : np.ndarray
        The mixed strategy that the player has. If it's None, it is set to an uniformly random one.

    Attributes
    ----------
    game : normal_game.OneShotGame
        The game the player participates.
        It is a class variable.
    player : int
        The player in the game.
    num_actions : int
        The number of actions the player has.
    cum_regrets : np.ndarray
        The cumulative regret.
    strategy : np.ndarray
        The mixed strategy.
    num_played : int
        The number of games the player has played before.
    """

    # the game the player play
    game = normal_game.OneShotGame()

    def __init__(self, player, strategy=None):
        if self.game is not None:
            self.initilize_player(player, strategy)
        else:
            raise normal_game.NotSetGameError("The game is not set")

    def initilize_player(self, player, strategy):
        if player > self.game.num_players:
            raise normal_game.ExceedNumPlayersError(f"Your input player exceeds the number of players in the given game. "
                                                    f"The limit is {self.game.num_players}, but your input is {player}")

        self.player = player
        self.num_actions = self.game.num_strategies[self.player]
        self.cum_regrets = np.zeros(self.num_actions)
        self.cum_strategy = np.zeros(self.num_actions)
        self.num_played = 0
        if strategy is None:
            self.strategy = np.tile(1.0 / self.num_actions, self.num_actions)
        else:
            self.strategy = strategy

    def init_game(cls, game_matrix):
        """initiate the normal game"""
        cls.game.initialize_game(game_matrix)

    def simulate_game(self, other_players):
        """
        Simulate the game given as `game`.

        Parameters
        ----------
        other_players : np.ndarray
            The other players that participate the game.

        Returns
        -------
        resultant_utilities : np.ndarray
            The utilities that each player gains after playing the game.
        played_actions : np.ndarray
            The actions that each player actually played in the game.
        """

        # check if other players are actually players
        if not np.array([isinstance(player, Player) for player in other_players]).all():
            raise NotPlayerError("The inputs are inavlid. The acceptable type is only Player.")

        other_players = list(other_players)
        all_players = other_players + [self]
        all_players.sort(key=lambda player: player.player)
        mixed_strategies = np.array([player.strategy for player in all_players])
        resultant_utilities, played_actions = self.game.play_prob(mixed_strategies)

        self.num_played += 1
        self.cum_strategy += self.strategy
        return resultant_utilities, played_actions

    def update_strategy(self):
        """
        Update the mixed strategy that the player has based on the cumulative regret.
        """

        self.strategy = self._regret_to_strategy()

    def _regret_to_strategy(self):
        """
        Transform the cumulative regret into the mixed strategy.
        If the cumulative regret is non-positive, the mixed strategy is uniformly random.

        Returns
        -------
        mixed_strategy : np.ndarray
            The mixed strategy.
        """

        # If the cumulative regret is 0, his/her mixed strategy is uniformly random.
        mixed_strategy = np.copy(self.cum_regrets)
        mixed_strategy[mixed_strategy < 0] = 0
        if (mixed_strategy.sum() <= 0):
            mixed_strategy = np.tile(1.0 / self.num_actions, self.num_actions)
        else:
            mixed_strategy = mixed_strategy / mixed_strategy.sum()
        return mixed_strategy

    def _calc_regrets(self, played_actions):
        """Calculate the regret according to actions that are played."""
        regrets = []
        add_regret = regrets.append
        helper_func.check_list_like(played_actions)
        base_utility = self.game.play_pure_strategy(played_actions)[self.player]
        for action in range(self.num_actions):
            played_actions[self.player] = action
            regret = self.game.play_pure_strategy(played_actions)[self.player] - base_utility
            add_regret(regret)

        return np.array(regrets)

    def update_cum_regret(self, played_pure_strategies):
        """Update the cumulative regret. If regret is negative, it is reduced to 0."""
        regrets = self._calc_regrets(played_pure_strategies)
        # regrets[regrets < 0] = 0
        self.cum_regrets += regrets

class NotPlayerError(Exception):
    def __init__(self, message):
        self.message = message
