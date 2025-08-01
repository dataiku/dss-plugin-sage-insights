import streamlit as st
import pandas as pd
import plotly.express as px

from sage.insights.data_structures import structures
from sage.src import dss_funcs, dss_folder

local_client = dss_funcs.build_local_client()
project_handle = local_client.get_default_project()
sage_project_key = project_handle.project_key

def main(df=pd.DataFrame()):
    """
    Dataiku Active Profile Usage
    """
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
    df = df.groupby(["instance_name", "userProfile"])["login"].nunique()
    df = df.reset_index(name="profile_count")

    # Initial fig
    fig = px.bar(
        df,
        x="userProfile",
        y="profile_count",
        color="instance_name",
        barmode="group",
        text="profile_count",
        labels={"userProfile": "Dataiku profile", "profile_count": "Cumulative Profile Usage"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # Customize layout for polish
    fig.update_layout(
        legend_title="Instance Names"
    )

    # Add text annotations inside bars
    fig.update_traces(textposition="outside")

    # Build the FIG construct to return
    FIG = structures.get("plotly")
    FIG["title"] = "Dataiku Active Profile Usage"
    FIG["data"] = fig
    
    return FIG