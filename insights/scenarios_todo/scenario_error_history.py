import pandas as pd
from sage.src import dss_folder


def main(df):
    j = {
        "chart_type": "DF",
        "split": False,
        "split_on": []
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
    filtered = df[df["run_outcome"] != "SUCCESS"]
    if filtered.empty:
        return [False, "No data"]
    grouped = filtered.groupby('scenario_id')['step_error_message'].value_counts()
    percentage_split = grouped.groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
    percentage_split_df = percentage_split.unstack()
    percentage_split_df = percentage_split_df.reset_index(drop=True)
    percentage_split_df = percentage_split_df.rename_axis(None, axis=1)
    percentage_split_df = percentage_split_df.T
    new_header = percentage_split_df.iloc[0]
    percentage_split_df.columns = new_header
    percentage_split_df = percentage_split_df[1:]
    return [True, percentage_split_df]