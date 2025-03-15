import pandas as pd
from sklearn.datasets import make_classification
from src.model_building_evaluation_functions import *

def test_randomized_search_loop():

    """
    Make sure that the results table should have a length equal to that of how many iterations are ran (30)
    """

    X, y = make_classification(random_state=10)
    results = randomized_search_loop(X, y)
    assert (len(results) == 30)