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

# train model and save the output 
def train_and_save_model(X_train, y_train, model_path, random_state=42,
                         n_estimators=200, min_samples_leaf=2, task="regression"):
    
    # create random forest pipeline 
    model = make_random_forest(random_state, n_estimators, min_samples_leaf, task=task)
    
    # train using training data and predict model 
    model.fit(X_train, y_train)
    
    # predict 
    predictions = model.predict(X_train)
    
    # ensure prediction not invalid
    assert np.isfinite(predictions).all(), 'RF produced invalid predictions.'
    
    # save output 
    destination = Path(model_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, destination)
    print(f'RF checkpoint: train_rows={len(X_train)}, features={X_train.shape[1]}, '
          f'train_prediction_range=({predictions.min():.3f}, {predictions.max():.3f})')
    print(f'Saved random forest to: {destination.resolve()} | exists={destination.exists()}')
    return model