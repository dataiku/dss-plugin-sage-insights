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
    Top 10 Active Users (GIT) over the last 365 Days
    """

    # Load additional data
    df = dss_folder.read_local_folder_input(
        sage_project_key = sage_project_key,
        project_handle = project_handle,
        folder_name="base_data",
        path=f"/users/rolling_git_history.csv"
    )

    # Logic
    from datetime import datetime, timedelta
    today = datetime.now()
    one_year_ago = today - timedelta(days=365)
    df = df[df["timestamp"] >= one_year_ago]
    df = df[~df["author"].str.contains("api:")]
    df = df.groupby(["instance_name", "author"])["count"].sum().sort_values(ascending=False)
    df = df.groupby("instance_name").head(10)
    df = df.reset_index()
    df = df.sort_values(by=["instance_name", "count"])

    # Initial fig
    fig = px.bar(
        df,
        x="author",
        y="count",
        color="instance_name",
        barmode="group",
        text="count",
        labels={"count": "Number of total GIT commits"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # Customize layout for polish
    fig.update_layout(
        xaxis_title="Dataiku login",
        yaxis_title="Total GIT Commits",
        legend_title="Instance Names"
    )

    # Add text annotations inside bars
    fig.update_traces(textposition="outside")

    # Build the FIG construct to return
    FIG = structures.get("plotly")
    FIG["title"] = "Top 10 Active Users (GIT) over the last 365 Days"
    FIG["data"] = fig

    return FIG