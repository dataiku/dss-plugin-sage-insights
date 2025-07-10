import streamlit as st
import pandas as pd
from sage.src import dss_folder
from sage.insights.data_structures import structures

def main(df=pd.DataFrame()):
    # load data structure
    data = structures.get("metric")

    # Load additional data
    if df.empty:
        df = dss_folder.read_folder_input(
            folder_name="base_data",
            path=f"/users/metadata.csv" # change this line
        )

    # Perform logic here
    total_users = df["login"].nunique()
    enabled_users = int(df.groupby("enabled")["login"].nunique().loc[True])
    delta_users = total_users - enabled_users
    total_users, enabled_users, delta_users

    # Set values
    data["label"] = "Total Users"
    data["data"] = total_users
    data["delta"] = delta_users

    return data