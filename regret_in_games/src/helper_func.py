import numpy as np
import pandas as pd

def check_list_like(input_array):
    """
    Check the input is list-like or not.

    Parameters
    ----------
    input_array : object
    """

    if not isinstance(input_array, (list, tuple, np.ndarray, pd.DataFrame, pd.Series)):
        raise TypeError(f"input's type should be list, tuple, numpy.ndarray, pd.DataFrame, or pd.Series. Your input: {type(input_array)}")
