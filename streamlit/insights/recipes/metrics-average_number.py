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
    fig = structures.get("metric")

    # Load additional data
    if df.empty:
        df = dss_folder.read_local_folder_input(
            sage_project_key = sage_project_key,
            project_handle = project_handle,
            folder_name="base_data",
            path=f"/recipes/metadata.csv" # change this line
        )

    # Perform logic here

    # Set values
    fig["label"] = "Average number of Recipes per Project"
    fig["data"] = round(df.groupby("project_key")["recipe_name"].size().mean(), 0)

    return fig