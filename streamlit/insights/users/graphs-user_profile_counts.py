import streamlit as st
import pandas as pd
import plotly.express as px

from sage.insights.data_structures import structures
from sage.src import dss_funcs, dss_folder

local_client = dss_funcs.build_local_client()
project_handle = local_client.get_default_project()
sage_project_key = project_handle.project_key

def main(df=pd.DataFrame()):
    # load data structure
    data = structures.get("bar_chart") # change this line

    # Load additional data
    if df.empty:
        df = dss_folder.read_local_folder_input(
            sage_project_key = sage_project_key,
            project_handle = project_handle,
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