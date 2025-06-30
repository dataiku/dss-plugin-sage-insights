import pandas as pd

def main(df=None, df_filter={}):
    # basic User counts
    total_users = df["login"].nunique()
    enabled_users = int(df.groupby("enabled")["login"].nunique().loc[True])
    delta_users = total_users - enabled_users
    total_users, enabled_users, delta_users

    meta = {
        "pass": True,
        "type": "metric",
        "title": "Enabled Users",
        "delta": 0,
        "value": enabled_users
    }
    return [meta, None]