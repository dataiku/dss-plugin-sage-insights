import pandas as pd


def main(df=None, df_filter={}):
    meta = {
        "pass": True,
        "type": "metric",
        "title": "Total number of Recipes",
        "delta": 0,
        "value": df["recipe_name"].nunique()
    }
    return [meta, None]