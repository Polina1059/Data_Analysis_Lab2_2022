from sklearn.svm import *
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import *
from sklearn.preprocessing import *
from sklearn.compose import *
from sklearn.pipeline import *
from sklearn.metrics import *
from sklearn.impute import *
from catboost import CatBoostRegressor


import src.config as cfg
from category_encoders.count import CountEncoder


cat_pipe = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='NA')),
    ('ohe', OneHotEncoder(handle_unknown='ignore', sparse=False))
])

real_pipe = Pipeline([
    ('imputer', SimpleImputer()),
    ('scaler', StandardScaler())
]
)

preprocess_pipe = ColumnTransformer(transformers=[
    ('real_cols', real_pipe, cfg.REAL_COLS),
    ('cat_cols', cat_pipe, cfg.CAT_COLS),
    ('cat_cols_ce', CountEncoder(), cfg.CAT_COLS),
]
)

model = CatBoostRegressor(iterations = 1000, learning_rate = 0.01, eval_metric = 'RMSE',
            random_seed = 37, loss_function = 'RMSE', l2_leaf_reg = 100,
            depth=4, rsm = 0.6, random_strength = 2)

catboost_regr_model = Pipeline([
    ('preprocess', preprocess_pipe),
    ('model', model)
]
)

model1 = LinearRegression()

linear_regr_model = Pipeline([
    ('preprocess', preprocess_pipe),
    ('model', model1)
]
)
