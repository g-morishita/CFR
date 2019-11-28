import numpy as np
import math
import helper_func


class OneShotGame:
    """
    Class to keep the information on the normal-form game.

    Parameters
    ----------
    game_matrix : list-like
        The matrix that represents the normal-form game.

    Attributes
    ----------
    game_matrix : numpy.ndarray
        The matrix that represents the normal-form game.
    num_strategies : int
        The number of strategies that each player has.
    num_players : int
        The number of players in the game.

    Examples
    ----------
    >>> import numpy as np
    >>> rsp_game_matrix = np.array([
    ...    [[0, 0], [-1, 1], [1, -1]],
    ...    [[1, -1], [0, 0], [-1, 1]],
    ...    [[-1, 1], [1, -1], [0, 0]]
    ...])
    >>> rsp = OneShotGame(rsp_game_matrix)
    >>> rsp.game_matrix
    array([[[ 0,  0],
        [-1,  1],
        [ 1, -1]],

       [[ 1, -1],
        [ 0,  0],
        [-1,  1]],

       [[-1,  1],
        [ 1, -1],
        [ 0,  0]]])
    >>> rsp.num_players
    2
    >>> rsp.num_strategies
    array([3, 3])
    """

    def __init__(self, game_matrix=None):
        if game_matrix is not None:
            self.initialize_game(game_matrix)
        else:
            self.game_matrix = None


    def initialize_game(self, game_matrix):
        """
        Initialize the game.

        Parameters
        ----------
        game_matrix : numpy.ndarray
            The matrix that represents the normal-form game.

        Returns
        -------
        self : returns an instance of self.
        """

        helper_func.check_list_like(game_matrix)
        self.game_matrix = np.array(game_matrix)

        # num_strategies is a np.ndarray. Its (i-1)th element is the number of strategies for player i.
        self.num_strategies = np.array(self.game_matrix.shape)[:-1]
        self.num_players = len(self.num_strategies)
        return self

    def _check_valid_game(self):
        """Check the game is set or not. If not, raise `NotSetGameError`."""
        if self.game_matrix is None:
            raise NotSetGameError("The game is not set.")

    def play_prob(self, mixed_strategies):
        """
        Play the game with given mixed strategies.

        Parameters
        ----------
        mixed_strategies : numpy.ndarray
            The mixed strategies of all players.
            For example, two players 1 and 2 play Rock-Paper-Scissors game.
            Player 1 has a mixed strategy (1/3, 1/2, 1/6).
            Player 2 has a mixed strategy (1/2, 1/2, 0).
            Then, you should give a parameter np.array([[1/3, 1/2, 1/6], [1/2, 1/2, 0]]).

        Returns
        -------
        resultant_utilities : np.ndarray
            The utilities that each player gains after the game `self.game_matrix`.
            Note that the game is actually played, so these utilities are not expected utilites of the strategies.

        played_pure_strategies : np.ndarray
            The actions that each player actually played.
        """

        self._check_valid_game()
        helper_func.check_list_like(mixed_strategies)
        mixed_strategies = np.array(mixed_strategies)
        if mixed_strategies.shape[0] > self.num_players:
            raise ExceedNumPlayersError(f"Your input exceeds the number of players in the given matrix game. Expected: {self.num_players}. Yours: {mixed_strategies.shape[0]}")

        played_pure_strategies = [self._get_strategy(player, mix_strategy) for player, mix_strategy in enumerate(mixed_strategies)]
        resultant_utilities = self.play_pure_strategy(played_pure_strategies)
        return resultant_utilities, played_pure_strategies


    def play_pure_strategy(self, pure_strategies):
        """
        Play the game with given pure strategies.

        Parameters
        ----------
        pure_strategies : np.ndarray
            The pure strategies that players play in the game.

        Returns
        -------
        resultant_utilities : int | float
            The utilities that each player gains after the game `self.game_matrix`.
        """

        helper_func.check_list_like(pure_strategies)
        pure_strategies = np.array(pure_strategies)

        if pure_strategies.shape[0] != self.num_strategies.shape[0]:
            raise NotMatchNumStrategiesError(f"The given number of strategies is {pure_strategies.shape[0]}, but the required one is {self.num_strategies}.")

        # check if the specified action does not exceed the number of actions in the given matrix game.
        if (self.num_strategies <= pure_strategies).any():
            raise ExceedActionSpaceError(f"The action you specified exceeds the number of actions in the given matrix game.{pure_strategies[(self.num_strategies <= pure_strategies)]}")
        # tuple() is required.　https://stackoverflow.com/questions/5508352/indexing-numpy-array-with-another-numpy-array
        resultant_utilities = self.game_matrix[tuple(pure_strategies)]
        return resultant_utilities


    def _get_strategy(self, player, mixed_strategy):
        """
        Get an action drawn from the mixed strategy's distribution.
        """

        helper_func.check_list_like(mixed_strategy)
        mixed_strategy = np.array(mixed_strategy)
        if not math.isclose(np.sum(mixed_strategy), 1.0):
            raise NotDistError(f"Your mixed strategy is not a probability distribution because its sum is not 1, but {np.sum(mixed_strategy)}")
        if player > self.num_players:
            raise ExceedNumPlayersError(f"Your input exceeds the number of players in the given matrix game. Expected: {self.num_players}. Yours: {player}")
        if self.num_strategies[player - 1] != mixed_strategy.shape[0]:
            raise NotMatchNumStrategiesError(f"The given number of strategies is {mixed_strategy.shape[0]}, but the required one is {self.num_strategies[player]}.")
        
        # choose an action according to the given mixed stratgy
        chose_action = np.searchsorted(mixed_strategy.cumsum(), np.random.uniform())
        return chose_action

class NotMatchNumStrategiesError(Exception):
    """
    Raise when you tried to play, the required number of strategies is not equal to that of strategies you gave. 
    """
    def __init__(self, message):
        self.message = message


class ExceedActionSpaceError(Exception):
    """
    Raise when you tried to specify a certain action, but the number exceeds the possible number of actions.
    """
    def __init__(self, message):
        self.message = message


class NotDistError(Exception):
    """
    Raise when the sum of your probability distribution is not 1.
    """
    def __init__(self, message):
        self.message = message


class ExceedNumPlayersError(Exception):
    """
    Raise when you manipulate player which exceeds the number of players in a given matrix game
    """
    def __init__(self, message):
        self.message = message


class NotSetGameError(Exception):
    """
    raise when the game is None, that is, the game is not set.
    """
    def __init__(self):
        self.message = "The game is not set!"
