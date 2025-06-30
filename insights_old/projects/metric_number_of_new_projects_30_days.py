import pandas as pd
from datetime import date, timedelta

def main(df=None, df_filter={}):
    meta = {
        "pass": True,
        "type": "metric",
        "title": "Total new projects last 30 days",
        "delta": 0,
        "value": len(df[df["creationOn"].dt.date >= (date.today() - timedelta(30))]["project_key"])
    }
    return [meta, None]