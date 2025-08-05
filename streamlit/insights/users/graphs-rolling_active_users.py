import pandas as pd
import plotly.express as px
from sage.src import dss_streamlit
from sage.insights.data_structures import structures


def main(filters = {}):
    # read the base layer data -- Change path for different data
    df = dss_streamlit.filter_base_data("/users/rolling_active_users.csv", filters)

    # Perform logic here
    df["month"] = df["timestamp"].dt.to_period("M")
    df = df.groupby(["instance_name", "month"])["count"].mean().round(0).reset_index()
    df["month"] = df["month"].dt.to_timestamp()

    # Initial fig
    fig = px.line(
        df,
        x="month",
        y="count",
        color="instance_name",
        text="count",
        labels={"count": "total active users"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # Customize layout for polish
    fig.update_layout(
        xaxis_title="Date Range",
        yaxis_title="Total Active Users",
        legend_title="Instance Names"
    )

    # Add text annotations inside bars
    fig.update_traces(textposition="top center")
    
    # Build the FIG construct to return
    FIG = structures.get("plotly")
    FIG["title"] = "Average monthly Active User login"
    FIG["data"] = fig
    
    return FIG