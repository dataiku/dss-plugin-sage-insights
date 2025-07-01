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
            path=f"/{st.session_state.instance_name}/users/metadata.csv" # change this line
        )

    # Perform logic here
    from datetime import date, timedelta
    today = date.today()
    for n in [30, 60, 90, 365]:
        activity = df[df["last_session_activity"].dt.date >= (today - timedelta(n))]
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
    df = df_transposed[1:]
    df = df.set_index("userProfile")
    df = df.rename_axis("count")

    # Build the data structure
    data["title"] = "Number of Users by Session Activity per Days"
    data["data"] = df
    data["x_label"] = "Number of Days"
    data["y_label"] = "Number of Users Active"

    return data