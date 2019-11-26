import numpy as np
import pandas as pd

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
        if not isinstance(game_matrix, (list, tuple, np.ndarray, pd.DataFrame, pd.Series)):
            TypeError(f"game_matrix's type should be list, tuple, numpy.ndarray, pd.DataFrame, or pd.Series. Your input: {type(game_matrix)}")
        self.game_matrix = np.array(game_matrix)

        # num_strategies is a np.ndarray. Its (i-1)th element is the number of strategies for player i.
        self.num_strategies = np.array(self.game_matrix.shape)[:-1]
        self.num_players = len(self.num_strategies)

