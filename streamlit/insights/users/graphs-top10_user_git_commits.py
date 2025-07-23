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
    Top 10 users with GIT commits
    """

    # Load additional data
    df = dss_folder.read_local_folder_input(
        sage_project_key = sage_project_key,
        project_handle = project_handle,
        folder_name="base_data",
        path=f"/users/commits.csv"
    )
    from datetime import datetime, timedelta

    # Perform logic here
    today = datetime.now()
    one_year_ago = today - timedelta(days=365)
    df = df[df["last_commit_date"] >= one_year_ago]
    df = df.groupby(["login", "instance_name"])["num_commits"].sum().sort_values(ascending=False)
    df = df.groupby("instance_name").head(10)
    df = df.reset_index()

    # Initial fig
    fig = px.bar(
        df,
        x="login",
        y="num_commits",
        color="instance_name",
        barmode="group",
        text="num_commits",
        labels={"num_commits": "Number of GIT commits"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # Customize layout for polish
    fig.update_layout(
        xaxis_title="Login Name",
        yaxis_title="Total GIT Commits",
        legend_title="Top 10 Users with GIT commits",
        template="plotly_white",
        font=dict(size=14),
        bargap=0.15,
        bargroupgap=0.1
    )

    # Add text annotations inside bars
    fig.update_traces(textposition="outside")

    # Build the FIG construct to return
    FIG = structures.get("plotly")
    FIG["title"] = "Top 10 Users with GIT commits over the last Year"
    FIG["data"] = fig

    return FIG