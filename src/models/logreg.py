# Logistic regression - Task 1 baseline

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

def make_logistic_regression():
    return Pipeline([
        ("imputer", SimpleImputer(strategy="median", keep_empty_features=True)),  # fill missing values with training-fold medians
        ("scaler", StandardScaler()),                                             # put features on the same scale
        ("model", LogisticRegression(max_iter=1000)),                             # the classifier itself
    ])
