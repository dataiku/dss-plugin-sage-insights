import pandas as pd
from datetime import date, timedelta


def main(df=None, df_filter={}):
    # MetaData JSON
    meta = {
        "pass": True,
        "type": "bar", # metric, bar
        "title": "Number of Users by GIT Actions per 'X' Days"
    }
    today = date.today()
    for n in [30, 60, 90, 365]:
        activity = df[df["last_commit_date"].dt.date >= (today - timedelta(n))]
        counts = activity.groupby(["userProfile"]).agg(
            count_value = ("login", "count")
        ).reset_index()
        counts.columns = ["userProfile", n]
        if n == 30:
            total_counts = counts
            continue
        total_counts = pd.merge(total_counts, counts, on=["userProfile"], how="left")

    df_transposed = total_counts.T.reset_index()
    new_columns = df_transposed.iloc[0].tolist()
    df_transposed.columns = new_columns
    df_final = df_transposed[1:]
    df_final = df_final.set_index("userProfile")
    df_final = df_final.rename_axis('count')
    df_final["CONSUMER"] = df_final["FULL_DESIGNER"] * 2
    return [meta, df_final]