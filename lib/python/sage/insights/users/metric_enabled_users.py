import pandas as pd
from sage.src import dss_folder

def main(df=None, df_filter={}):
    df = dss_folder.read_folder_input(path = "instance/_dataiku_users.csv")
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