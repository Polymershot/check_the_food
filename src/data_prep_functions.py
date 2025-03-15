import pandas as pd

def impute_zeros(df:pd.DataFrame, last_n_cols:int) -> pd.DataFrame:

    """
    Imputes a Pandas Dataframe with 0's for the last "n" columns

    Args:
        df (pd.DataFrame): Pandas Dataframe (Tabular)
        last_n_cols (int): Positive integer indicating first column from which you want to impute {n: end of data}

    Returns:
        pd.DataFrame: imputed Pandas Dataframe
    """
    col_list = list(df.iloc[:, -last_n_cols:].columns)
    df[col_list] = df[col_list].fillna(0)
    return df


def union_join(df1:pd.DataFrame, df2:pd.DataFrame) -> pd.DataFrame:

    """
    Implements a union-like join to vertically join two Pandas Dataframes that have the exact same columns

    Args:
        df1 (pd.Dataframe): Must contain same columns as df2
        df2 (pd.DataFrame): Must contain same columns as df1

    Returns:
        pd.DataFrame: Returns the "union" of df1 and df2
    """

    combined_df = pd.concat([df1, df2])
    return combined_df

