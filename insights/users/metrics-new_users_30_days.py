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
    from datetime import date, timedelta
    new_users = len(df[df["creationDate"].dt.date >= (date.today() - timedelta(30))]["login"])

    # Set values
    data["label"] = "New Users last 30 days"
    data["data"] = new_users

    return data