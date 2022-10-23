from sklearn.svm import *
from sklearn.model_selection import *
from sklearn.preprocessing import *
from sklearn.compose import *
from sklearn.pipeline import *
from sklearn.metrics import *
from sklearn.impute import *
from catboost import CatBoostRegressor


import src.config as cfg
import category_encoders as ce


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
    ('woe_cat_cols', ce.WOEEncoder(), cfg.CAT_COLS),
    ('ohe_cols', 'passthrough', cfg.OHE_COLS)
]
)

model = CatBoostRegressor(iterations=1000, learning_rate=0.5)

catboost_regr_model = Pipeline([
    ('preprocess', preprocess_pipe),
    ('model', model)
]
)

model1 = LinearSVR()

linear_svr_model = Pipeline([
    ('preprocess', preprocess_pipe),
    ('model', model1)
]
)
