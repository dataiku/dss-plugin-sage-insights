import streamlit as st
import pandas as pd
from sage.src import dss_folder
from sage.insights.data_structures import structures

def main(df=pd.DataFrame()):
    # load data structure
    data = structures.get("bar_chart") # change this line

    # Load additional data
    if df.empty:
        df = dss_folder.read_folder_input(
            folder_name="base_data",
            path=f"/{st.session_state.instance_name}/scenarios/run_history.csv" # change this line
        )

    # Perform logic here
    filtered = df[~df["run_outcome"].str.contains("SUCESS", na=False)]
    if filtered.empty:
        data["pass"] = False
        return data
    grouped = filtered.groupby('scenario_id')['step_error_message'].value_counts()
    percentage_split = grouped.groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
    percentage_split_df = percentage_split.unstack()
    percentage_split_df = percentage_split_df.reset_index(drop=True)
    percentage_split_df = percentage_split_df.rename_axis(None, axis=1)
    percentage_split_df = percentage_split_df.T
    new_header = percentage_split_df.iloc[0]
    percentage_split_df.columns = new_header
    percentage_split_df = percentage_split_df[1:]

    # Build the data structure
    data["title"] = "Number of Users by GIT Actions per 'X' Days"
    data["pass"] = False
    return data