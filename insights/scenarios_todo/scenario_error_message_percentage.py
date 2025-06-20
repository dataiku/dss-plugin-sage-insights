import pandas as pd
from sage.src import dss_folder


def main(df_filter={}):
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
    filtered = df[df['run_outcome'] != 'SUCCESS']
    if filtered.empty:
        return [False, "No data"]
    grouped = filtered.groupby('scenario_id')['step_error_message'].unique()
    common_errors_df = grouped.explode().reset_index()
    common_errors_df.dropna(subset=['step_error_message'], inplace=True)
    return [True, common_errors_df]