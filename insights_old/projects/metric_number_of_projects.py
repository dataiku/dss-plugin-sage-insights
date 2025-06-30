import pandas as pd

def main(df=None, df_filter={}):
    meta = {
        "pass": True,
        "type": "metric",
        "title": "Total DSS Projects",
        "delta": 0,
        "value": df["project_key"].nunique()
    }
    return [meta, None]