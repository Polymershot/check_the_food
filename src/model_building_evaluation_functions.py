from sklearn.model_selection import RandomizedSearchCV
from imblearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from imblearn.over_sampling import BorderlineSMOTE
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
import pandas as pd

def randomized_search_loop(x_train:pd.DataFrame, y_train:pd.Series) -> pd.DataFrame:
    
    """
    Implements a RandomSearch to compare multiple models as well as create different parameter combinations for each model

    Args:
        x_train (pd.DataFrame): Input variables
        y_train (pd.Series): Output variable

    Returns:
        pd.DataFrame: Returns a dataframe of the results sorted in descending order according to the scoring metric
    """
    # Pipeline to streamline process
    pipeline = Pipeline ([
        ('smote',  BorderlineSMOTE(sampling_strategy='not majority')),
        ('model', 'passthrough')
    ])


    # Hyperparameter combinations
    param_grid = [
        {
            'model': [RandomForestClassifier()],
            'model__n_estimators': [10, 100, 500],
            'model__criterion': ['gini', 'entropy', 'log_loss'],
            'model__max_depth': [2,10,50, None]

        },

        {
            'model': [XGBClassifier()],
            'model__eta': [0.1,0.3,0.5],
            'model__gamma': [0.1, 0.3, 1],
            'model__max_depth': [2,6,10],
            'model__alpha': [0,1]

        },

        {
            'model': [LogisticRegression()]
        }
    ]

    # Initiate the search
    cv = StratifiedKFold(n_splits=3)
    grid = RandomizedSearchCV(pipeline, n_iter=30, param_distributions=param_grid, cv=cv, n_jobs=-1,scoring='f1_macro', refit=False)
    grid_data = grid.fit(x_train, y_train)
    results = pd.DataFrame(grid_data.cv_results_)
    return (results.sort_values(by=['rank_test_score']))