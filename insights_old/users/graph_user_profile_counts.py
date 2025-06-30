import pandas as pd
from datetime import date, timedelta


def main(df=None, df_filter={}):
    # MetaData JSON
    meta = {
        "pass": True,
        "type": "bar", # metric, bar
        "title": "Count of User Profiles by Active"
    }
    # Build DF for Chart
    filtered = df[df["enabled"] == True]
    df_final = filtered.groupby("userProfile")["login"].nunique()
    return [meta, df_final]