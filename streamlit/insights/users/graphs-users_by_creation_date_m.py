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
    Cumulative Number of Users by Creation Date (Monthly)
    """

    # Load additional data
    if df.empty:
        df = dss_folder.read_local_folder_input(
            sage_project_key = sage_project_key,
            project_handle = project_handle,
            folder_name="base_data",
            path=f"/users/metadata.csv"
        )

    # Logic Here
    df["creationMonth"] = df["creationDate"].dt.to_period("M")
    df = df[df["creationDate"] != "1970-01-01"].reset_index()
    df = df.groupby(by=["instance_name", "creationMonth"])["login"].size().reset_index(name="user_count")
    cumsum = df.groupby("instance_name")["user_count"].cumsum()
    df = pd.concat([df.drop(columns=["user_count"]), cumsum], axis=1)
    df["creationMonth"] = df["creationMonth"].dt.to_timestamp()

    # Create the figure here
    fig = px.line(
        df,
        x="creationMonth",
        y="user_count",
        color="instance_name",
        text="user_count",
        labels={"creationMonth": "Creation Date (Month)", "user_count": "Cumulative Users"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # Update layout
    fig.update_layout(
        xaxis_tickformat="%Y-%m",
        xaxis=dict(tickangle=-45),
        legend_title="Instance Names"
    )

    # Add text annotations inside bars
    fig.update_traces(textposition="top center")

    # Build the FIG construct to return
    FIG = structures.get("plotly")
    FIG["title"] = "Cumulative Number of Users by Creation Date (Monthly)"
    FIG["data"] = fig
    
    return FIG