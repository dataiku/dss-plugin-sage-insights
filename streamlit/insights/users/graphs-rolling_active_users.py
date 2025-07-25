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
    Rolling Active Users per Month Year
    """

    # Load additional data
    if df.empty:
        df = dss_folder.read_local_folder_input(
            sage_project_key = sage_project_key,
            project_handle = project_handle,
            folder_name="base_data",
            path=f"/users/rolling_commit_user_counts.csv"
        )

    # Perform logic here
    df = df.sort_values("date")

    # Initial fig
    fig = px.line(
        df,
        x="date",
        y="author",
        color="instance_name",
        text="author",
        labels={"author": "total active users"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # Customize layout for polish
    fig.update_layout(
        xaxis_title="Month Year",
        yaxis_title="Total Active Users",
        legend_title="Instance Names",
        template="plotly_white",
        font=dict(size=14),
        bargap=0.15,
        bargroupgap=0.1
    )

    # Add text annotations inside bars
    fig.update_traces(textposition="top center")

    # Build the FIG construct to return
    FIG = structures.get("plotly")
    FIG["title"] = "Rolling Active Users per Month Year"
    FIG["data"] = fig
    
    return FIG