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
            path=f"/users/metadata.csv" # change this line
        )

    # Perform logic here
    df = df[df["enabled"] == True]
    df = df.groupby("userProfile")["login"].nunique()

    # Build the data structure
    data["title"] = "Count of User Profiles by Active"
    data["data"] = df
    data["y_label"] = "Total Number of License"
    
    return data