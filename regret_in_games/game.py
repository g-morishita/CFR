import numpy as np
import pandas as pd

def _check_list_like(input_array):
    if not isinstance(input_array, (list, tuple, np.ndarray, pd.DataFrame, pd.Series)):
        raise TypeError(f"input's type should be list, tuple, numpy.ndarray, pd.DataFrame, or pd.Series. Your input: {type(input_array)}")

class OneShotGame:
    """
    This class represents matrix games. 
    This is applicable to n by n matrix game, but be careful for the order of utilities.
    For now, it's safe to use this for two by two matrix games.
    """
    def __init__(self, game_matrix):
        """
        game_matrix has to be a list-like object.
        """
        _check_list_like(game_matrix)
        self.game_matrix = np.array(game_matrix)

        # num_strategies is a np.ndarray. Its (i-1)th element is the number of strategies for player i.
        self.num_strategies = np.array(self.game_matrix.shape)[:-1]
        self.num_players = len(self.num_strategies)
    
    def play_prob(self, mixed_strategies):
        """
        Play the game with mixed strategies.
        The game is actually played and each player gets their utility.
        Note that the game is actually played, so the utility is not the expected one.
        """


    def _play_pure_strategy(self, pure_strategies):
        """
        play the game within the pure strategies and return the utilites
        """
        _check_list_like(pure_strategies)
        pure_strategies = np.array(pure_strategies)

        if pure_strategies.shape[0] != self.num_strategies:
            raise NotMatchNumStrategiesError(f"The given number of strategies is {pure_strategies.shape[0]}, but the required one is {self.num_strategies}.")

        # check if the specified action does not exceed the number of actions in the given matrix game.
        if (self.num_strategies <= pure_strategies).any():
            raise ExceedActionSpaceError(f"The action you specified exceeds the number of actions in the given matrix game.{pure_strategies[(self.num_strategies <= pure_strategies)]}")
        return self.game_matrix[pure_strategies]

    def _get_strategy(self, player, mixed_strategy):
        """
        According to mixed_strategy of player, you can get one strategy drawn from the mixed strategy's distribution.
        """
        _check_list_like(mixed_strategy)
        mixed_strategy = np.array(mixed_strategy)
        if not math.isclose(np.sum(mixed_strategy), 1.0):
            raise NotDistError(f"Your mixed strategy is not a probability distribution because its sum is not 1, but {np.sum(mixed_strategy)}")
        if player > self.num_players:
            raise ExceedNumPlayersError(f"Your input exceeds the number of players in the given matrix game. Expected: {self.num_players}. Yours: {player}")
        
        # choose an action according to the given mixed stratgy
        chose_action = np.searchsorted(mixed_strategy.cumsum(), np.random.uniform())
        return chose_action


def NotMatchNumStrategiesError(Exception):
    """
    Raised when you tried to play, the required number of strategies is not equal to that of strategies you gave. 
    """
    def __init__(self, message):
        self.message = message


def ExceedActionSpaceError(Exception):
    """
    Raised when you tried to specify a certain action, but the number exceeds the possible number of actions.
    """
    def __init__(self, message):
        self.message = message


def NotDistError(Exception):
    """
    Raise when the sum of your probability distribution is not 1.
    """
    def __init__(self, message):
        self.message = message


def ExceedNumPlayersError(Exception):
    """
    Raised when you manipulate player which exceeds the number of players in a given matrix game
    """
    def __init__(self, message):
        self.message = message
