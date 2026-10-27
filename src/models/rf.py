# Random forest classifier + regressor
from pathlib import Path
import numpy as np 
import joblib
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

# create model 
def make_random_forest(random_state=42, n_estimators=200, 
                       min_samples_leaf=2, task="regression"):
    
    if task == "classification": # random forest supports classification for task 1
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            min_samples_leaf=min_samples_leaf,
            random_state=random_state,
            n_jobs=-1
        )

    elif task == "regression": # random forest supports regression for task 2
        model = RandomForestRegressor(
            n_estimators=n_estimators,
            min_samples_leaf=min_samples_leaf,
            random_state=random_state,
            n_jobs=-1
        )
        
    else: 
        raise ValueError("Task must be 'classification' or 'regression'.")

    return Pipeline([
        ("imputer", SimpleImputer(
            strategy="median",
            keep_empty_features=True
        )),
        ("model", model)
    ])
