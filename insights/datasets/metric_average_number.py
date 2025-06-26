import pandas as pd


def main(df=None, df_filter={}):
    meta = {
        "pass": True,
        "type": "metric",
        "title": "Average number of Datasets per Project",
        "delta": 0,
        "value": round(df.groupby("project_key")["dataset_name"].size().mean(), 0)
    }
    return [meta, None]