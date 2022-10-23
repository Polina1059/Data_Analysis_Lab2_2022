import pandas as pd


def has_pool(df: pd.DataFrame) -> pd.DataFrame:
    df['HasPool'] = (df['PoolArea'] > 0).astype(int)
    return df

# def has_fence(df: pd.DataFrame) -> pd.DataFrame:
#     print(df['Fence'])
#     df['HasFence'] = (df['Fence'] > 0).astype(int)
#     return df

def house_age(df: pd.DataFrame) -> pd.DataFrame:
    df['House_Age'] = df['YrSold'] - df['YearBuilt']
    return df

def featurization(df: pd.DataFrame) -> pd.DataFrame:
    df = has_pool(df)
    # df = has_fence(df)
    df = house_age(df)
    return df