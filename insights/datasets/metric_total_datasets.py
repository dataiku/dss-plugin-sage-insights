import pandas as pd


def main(df=None, df_filter={}):
    meta = {
        "pass": True,
        "type": "metric",
        "title": "Total number of Datasets",
        "delta": 0,
        "value": df["dataset_name"].nunique()
    }
    return [meta, None]