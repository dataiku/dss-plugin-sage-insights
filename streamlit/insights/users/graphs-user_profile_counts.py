import pandas as pd
import plotly.express as px
from sage.src import dss_streamlit
from sage.insights.data_structures import structures


def main(filters = {}):
    # read the base layer data -- Change path for different data
    df = dss_streamlit.filter_base_data("/users/metadata.csv", filters)

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