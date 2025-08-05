import pandas as pd
import plotly.express as px
from sage.src import dss_streamlit
from sage.insights.data_structures import structures


def main(filters = {}):
    # read the base layer data -- Change path for different data
    df = dss_streamlit.filter_base_data("/users/metadata.csv", filters)

    # Perform logic here
    df["month"] = df["last_session_activity"].dt.to_period("M")
    filtered_df = pd.DataFrame()
    for i,g in df.groupby(by="month"):
        tdf = g.groupby(["instance_name"]).size().reset_index(name="count")
        tdf["month"] = i
        if filtered_df.empty:
            filtered_df = tdf
        else:
            filtered_df = pd.concat([filtered_df, tdf], ignore_index=True)
    filtered_df = filtered_df[filtered_df["month"] != "1970-01"]
    filtered_df["month"] = filtered_df["month"].dt.to_timestamp()

    # Initial fig
    fig = px.bar(
        filtered_df,
        x="month",
        y="count",
        color="instance_name",
        barmode="group",
        text="count",
        labels={"count": "Users with last session activity"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # Customize layout for polish
    fig.update_layout(
        xaxis_title="Date Range",
        yaxis_title="Active Users",
        legend_title="Instance Names"
    )

    # Add text annotations inside bars
    fig.update_traces(textposition="outside")
    
    # Build the FIG construct to return
    FIG = structures.get("plotly")
    FIG["title"] = "All User Attrition Over Time"
    FIG["data"] = fig
    
    return FIG