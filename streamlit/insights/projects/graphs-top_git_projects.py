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
    filtered_df = df[df["timestamp"] >= one_year_ago]
    filtered_df = filtered_df[~filtered_df["login"].str.contains("api:")]
    filtered_df = filtered_df.groupby(["instance_name", "project_key"])["count"].sum().sort_values(ascending=False)
    filtered_df = filtered_df.groupby("instance_name").head(10)
    filtered_df = filtered_df.reset_index()
    filtered_df = filtered_df.sort_values(by=["instance_name", "count"])

    # Initial fig
    fig = px.bar(
        filtered_df,
        x="project_key",
        y="count",
        color="instance_name",
        barmode="group",
        text="count",
        labels={"count": "Number of total GIT commits"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # Customize layout for polish
    fig.update_layout(
        xaxis_title="Dataiku Project Key",
        yaxis_title="Total GIT Commits",
        legend_title="Instance Names"
    )

    # Add text annotations inside bars
    fig.update_traces(textposition="outside")

    # Build the FIG construct to return
    FIG = structures.get("plotly")
    FIG["title"] = "Top 10 Active Projects over the last 365 Days"
    FIG["data"] = fig

    return FIG