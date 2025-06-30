import pandas as pd
from datetime import date, timedelta

def main(df=None, df_filter={}):
    # basic User counts
    new_users = len(df[df["creationDate"].dt.date >= (date.today() - timedelta(30))]["login"])

    meta = {
        "pass": True,
        "type": "metric",
        "title": "New Users last 30 days",
        "delta": 0,
        "value": new_users
    }
    return [meta, None]