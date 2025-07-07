import streamlit as st
import pandas as pd
from sage.src import dss_folder
from sage.insights.data_structures import structures

def main(df=pd.DataFrame()):
    # load data structure
    data = structures.get("bar_chart")

    # Load additional data
    if df.empty:
        df = dss_folder.read_folder_input(
            folder_name="base_data",
            path=f"/datasets/metadata.csv"
        )
    df = df.groupby("dataset_type")[["project_key", "instance_name"]].count()
    df = df.reset_index()

    # Build the data structure
    data["title"] = "Filesystem % Usage"
    data["data"] = df
    data["x"] = "dataset_type"
    data["y"] = ["project_key", "instance_name"]
    data["x_label"] = "Number of Projects"
    data["y_label"] = "Connection Type"
    data["horizontal"] = True
    
    return data