import pandas as pd
import plotly.express as px
from sage.src import dss_streamlit
from sage.insights.data_structures import structures


def main(filters = {}):
    # read the base layer data -- Change path for different data
    df = dss_streamlit.filter_base_data("/users/rolling_git_history.csv", filters)

    # Perform logic here
    from datetime import datetime, timedelta
    today = datetime.now()
    one_year_ago = today - timedelta(days=365)
    df = df[df["timestamp"] >= one_year_ago]
    df = df[~df["login"].str.contains("api:")]
    df = df.groupby(["instance_name", "login"])["count"].sum().sort_values(ascending=False)
    df = df.groupby("instance_name").head(10)
    df = df.reset_index()
    df = df.sort_values(by=["instance_name", "count"])

    # Initial fig
    fig = px.bar(
        df,
        x="login",
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