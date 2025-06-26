import pandas as pd


def main(df=None, df_filter={}):
    meta = {
        "pass": True,
        "type": "metric",
        "title": "Total number of Scenarios",
        "delta": 0,
        "value": df["scenario_id"].count()
    }
    return [meta, None]