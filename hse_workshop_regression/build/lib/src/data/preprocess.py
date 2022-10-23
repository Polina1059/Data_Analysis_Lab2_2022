from typing import Tuple
import pandas as pd
import numpy as np
import src.config as cfg



def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:  # заполним пропущенные данные
    for col in cfg.CAT_COLS_TO_FILL:
        most_freq = df[col].value_counts().index[0]
        df[col] = df[col].fillna(most_freq)

    for name in df.select_dtypes("number"):
        df[name] = df[name].fillna(0)
        
    return df

def fix_wrong_values(df: pd.DataFrame) -> pd.DataFrame:    # исправим ошибки в данных
    df['Exterior2nd'].replace({"Brk Cmn": "BrkComm"}, inplace=True)
    df['BldgType'].replace({"Duplex": "Duplx"}, inplace=True)
    df['BldgType'].replace({"2fmCon": "2FmCon"}, inplace=True)
    df['BldgType'].replace({"Twnhs": "TwnhsI"}, inplace=True)
    return df

def set_idx(df: pd.DataFrame, idx_col: str) -> pd.DataFrame:
    df = df.set_index(idx_col)
    return df

def drop_unnecesary_id(df: pd.DataFrame) -> pd.DataFrame:
    if 'Id' in df.columns:
        df = df.drop('Id', axis=1)
    return df

def cast_types(df: pd.DataFrame) -> pd.DataFrame:
    df[cfg.CAT_COLS] = df[cfg.CAT_COLS].astype('category')

    ohe_int_cols = df[cfg.OHE_COLS].select_dtypes('number').columns
    df[ohe_int_cols] = df[ohe_int_cols].astype(np.int8)

    df[cfg.REAL_COLS] = df[cfg.REAL_COLS].astype(np.float32) 
    return df


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df = set_idx(df, cfg.ID_COL)
    df = drop_unnecesary_id(df)
    # df = add_ord_edu(df)
    df = cast_types(df)
    df = fill_missing_values(df)
    df = fix_wrong_values(df)
    return df   

def preprocess_target(df: pd.DataFrame) -> pd.DataFrame:
    df[cfg.TARGET_COL] = df[cfg.TARGET_COL].astype(np.int8)
    return df


def extract_target(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df, target = df.drop(cfg.TARGET_COL, axis=1), df[cfg.TARGET_COL]
    return df, target
