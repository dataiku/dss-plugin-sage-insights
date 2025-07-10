import streamlit as st
import pandas as pd
import plotly.express as px

from sage.src import dss_folder
from sage.insights.data_structures import structures

def main(df=pd.DataFrame()):
    # load data structure
    FIG = structures.get("plotly")

    # Load additional data
    if df.empty:
        df = dss_folder.read_folder_input(
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