import pandas as pd
from sage.src import dss_folder


def main(df_filter={}):
    j = {
        "chart_type": "PIE",
        "split": True,
        "split_on": ["scenario_id"]
    }

    # Load the data and cleanse anything -- FR
    df = dss_folder.read_folder_input(
        folder_name = "base_data",
        path = "/scenarios/_run_history.csv",
        data_type = "DF"
    )

    # Filter (Basic)
    if df_filter:
        for key in df_filter.keys():
            df = df[df[key] == df_filter[key]]

    # Run
    grouped = df.groupby('scenario_id')['run_outcome'].value_counts()
    percentage_split = grouped.groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
    percentage_split_df = percentage_split.unstack()
    percentage_split_df = percentage_split_df.reset_index(drop=True)
    percentage_split_df = percentage_split_df.rename_axis(None, axis=1)
    return [True, percentage_split_df]