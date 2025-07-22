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
            folder_name="base_data",
            path=f"/projects/metadata.csv" # change this line
        )

    # Perform logic here
    df['year'] = df['lastModifiedOn'].dt.year
    df['month'] = df['lastModifiedOn'].dt.month
    filtered_df = pd.DataFrame()
    for i,g in df.groupby(by=["year", "month"]):
        year, month = i
        tdf = g.groupby(["instance_name"]).size().reset_index(name="count")
        tdf["year_month"] = f"{year}-{month}"
        if filtered_df.empty:
            filtered_df = tdf
        else:
            filtered_df = pd.concat([filtered_df, tdf], ignore_index=True)
    filtered_df["year_month"] = pd.to_datetime(filtered_df["year_month"])

    # Initial fig
    fig = px.bar(
        filtered_df,
        x="year_month",
        y="count",
        color="instance_name",
        barmode="group",
        text="count",
        labels={"count": "number of active projects"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # Customize layout for polish
    fig.update_layout(
        xaxis_title="Year / Month",
        yaxis_title="Active Project Count",
        legend_title="Instance Name",
        template="plotly_white",
        font=dict(size=14),
        bargap=0.15,
        bargroupgap=0.1
    )

    # Add text annotations inside bars
    fig.update_traces(textposition="outside")

    # Build the FIG construct to return
    FIG["title"] = "Number of Active Projects Per Year / Month"
    FIG["data"] = fig
    
    return FIG