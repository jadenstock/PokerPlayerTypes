import tomllib
import pandas as pd
import numpy as np

def load_config(path="./etc/config.toml"):
    with open(path, "rb") as f:
        return tomllib.load(f)


def clean_and_convert(df, str_columns=["Player"], drop_columns=["My C Won"]):
    # Drop specified columns
    df = df.drop(columns=drop_columns)

    # Remove commas and dollar signs, replace "-" with NaN, and convert numeric columns to float
    for col in df.columns:
        if col not in str_columns:
            df[col] = df[col].replace({'$': '', ',': ''}, regex=True)
            # Replace standalone '-' with NaN
            df[col] = df[col].replace('^-$', np.nan, regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df


def fill_na_values(df, fill_method="zero"):
    """
    Fills NaN values in the dataframe. Options to fill with 0.0 or with column mean.

    Parameters:
    - df: Input dataframe
    - fill_method: Method to fill NaN values ("zero" for 0.0, "mean" for column mean)

    Returns:
    - df: Dataframe with NaN values filled
    """
    if fill_method == "zero":
        df = df.fillna(0.0)
    elif fill_method == "mean":
        df = df.apply(lambda col: col.fillna(col.mean()) if col.dtype in ['float64', 'int64'] else col)
    else:
        raise ValueError("Invalid fill_method. Use 'zero' or 'mean'.")
    return df


if __name__=="__main__":
    config = load_config()
    PN_REPORT = config['paths']['pn_report']
    data = pd.read_csv(PN_REPORT)
    data = clean_and_convert(data)
    print(data.head(10))
