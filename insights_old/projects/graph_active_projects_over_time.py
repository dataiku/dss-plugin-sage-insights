import pandas as pd
from datetime import date, timedelta


def main(df=None, df_filter={}):
    # MetaData JSON
    meta = {
        "pass": True,
        "type": "bar", # metric, bar
        "title": "Active Projects over Days"
    }
    # Build DF for Chart
    today = date.today()
    data = { "days": [], "count": [] }
    for n in [30, 60, 90, 365]:
        activity = df[df["lastModifiedOn"].dt.date >= (today - timedelta(n))]
        data["days"].append(n)
        data["count"].append(activity["project_key"].nunique())
    df_final = pd.DataFrame(data)
    df_final.set_index("days", inplace=True)
    return [meta, df_final]