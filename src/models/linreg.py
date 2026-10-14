# Linear regression - Task 2 baseline
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

# note: package does multiple linear regression automatically 

def make_linear_regression():
    return Pipeline([
        ('imputer', SimpleImputer(strategy='median', keep_empty_features=True)), #replaces missing predictors using training-fold medians.
        ('scaler', StandardScaler()), #standardises each predictor using training-fold statistics
        ('model', LinearRegression())
    ])