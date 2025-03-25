# Use python -m pytest to run from root directory
import pandas as pd
import numpy as np
from src.data_prep_functions import *

def test_impute_zeros():

    """
    Make sure that all missing values are imputed by zero for the last "n" columns
    """
    df = pd.DataFrame({'a': [1,2,3,4 ], 'b': [2,3, np.nan, 4], 'c': [3,57,2, np.nan]})
    df = impute_zeros(df, 2)
    assert all(df.iloc[-2:] == 0)

def test_union_join():

    """
    The number of rows for the resulting table should equal the number of rows for the relevant dataframes
    
    The number of columns should also stay the same
    """
    df1 = pd.DataFrame({'a': [1,2,3,4 ], 'b': [2,3, 1, 4], 'c': [3,57,2, 1]})
    df2 = pd.DataFrame({'a': [19,2,3,3 ], 'b': [1212,3, 0, 4], 'c': [-30,57,30, -101]})
    combined_df = union_join(df1, df2)
    assert (combined_df.shape[0] == (df1.shape[0] + df2.shape[0])) & (combined_df.shape[1] == df1.shape[1])
