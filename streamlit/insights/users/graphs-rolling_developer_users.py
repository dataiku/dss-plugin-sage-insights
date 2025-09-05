import pandas as pd
import plotly.express as px
from sage.src import dss_streamlit
from sage.insights.data_structures import structures


def main(filters = {}):
    # read the base layer data -- Change path for different data
    df = dss_streamlit.filter_base_data("/users/rolling_developer_user_logins.csv", filters)

    # Perform logic here
    if df["timestamp"].dt.to_period("M").nunique() > 3:
        title = "Average Monthly Developer User login"
        df["dt_range"] = df["timestamp"].dt.to_period("M")
        df = df.groupby(["instance_name", "dt_range"])["developer_user_logins"].nunique().reset_index(name="total_logins")
        df["dt_range"] = df["dt_range"].dt.to_timestamp()
    else:
        title = "Average Daily Developer User login"
        df["dt_range"] = df["timestamp"].dt.to_period("D")
        df = df.groupby(["instance_name", "dt_range"])["developer_user_logins"].nunique().reset_index(name="total_logins")
        df["dt_range"] = df["dt_range"].dt.to_timestamp()

    # Initial fig
    fig = px.line(
        df,
        x="dt_range",
        y="total_logins",
        color="instance_name",
        text="total_logins",
        labels={"total_logins": "total active users"},
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
    FIG["title"] = title
    FIG["data"] = fig
    
    return FIG