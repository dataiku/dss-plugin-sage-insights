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
    FIG = structures.get("plotly")

    # Load additional data
    if df.empty:
        df = dss_folder.read_local_folder_input(
            sage_project_key = sage_project_key,
            project_handle = project_handle,
            folder_name = "base_data",
            path = f"/disk_space/filesystem.csv"
        )
    df = df.groupby(["instance_name", "mounted_on"])["used_pct"].max().reset_index(name="used_pct")

    # Plot
    fig = px.bar(
        df,
        y="mounted_on",
        x="used_pct",
        color="instance_name",
        barmode="group",
        text="used_pct",
        labels={"count": "percent_used"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # Customize layout for polish
    fig.update_layout(
        yaxis_title="Mounted On",
        xaxis_title="Diskspace Used Percent",
        legend_title="Instance Name",
        template="plotly_white",
        font=dict(size=14),
        bargap=0.15,
        bargroupgap=0.1
    )

    # Add text annotations inside bars and background lines
    fig.update_traces(textposition="outside")
    fig.update_layout(
        xaxis=dict(showgrid=True, gridcolor='lightgray', zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='lightgray', zeroline=False)
    )

   # Build the FIG construct to return
    FIG["title"] = "Diskspace Used percent"
    FIG["data"] = fig
    
    return FIG