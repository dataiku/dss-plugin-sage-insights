
import streamlit as st
import pandas as pd
from sage.src import dss_folder
from sage.insights.data_structures import structures

def main(df_filter={}):
    # load data structure
    data = structures.get("metric")

    # Load additional data
    df = dss_folder.read_folder_input(
        folder_name="base_data",
        path=f"/{st.session_state.instance_name}/datasets/metadata.csv"
    )

    # Perform logic here

    # Set values
    data["label"] = "Total number of Datasets"
    data["data"] = df["dataset_name"].nunique()

    return data