import pandas as pd
import plotly.express as px
from sage.src import dss_streamlit
from sage.insights.data_structures import structures


def main(filters = {}):
    # read the base layer data -- Change path for different data
    df = dss_streamlit.filter_base_data("/scenarios/run_history.csv", filters)

    # Perform logic here
    filtered_df = df[~df["run_outcome"].str.contains("SUCESS", na=False)]
    grouped = filtered_df.groupby(["instance_name", 'scenario_id'])['step_error_message'].value_counts().reset_index(name="count")
    grouped["error_pct"] = grouped["count"].apply(lambda x: 100 * x / float(grouped["count"].sum()))
    grouped["error_pct"] = round(grouped["error_pct"], 2)
    grouped["instance_name.scenario_id"] = grouped["instance_name"] + "." + grouped["scenario_id"]
    del grouped["count"]

    # Initial fig
    fig = px.bar(
        grouped,
        x="instance_name",
        y="error_pct",
        color="instance_name.scenario_id",
        barmode="group",
        labels={"error_pct": "Error Percent"},
        hover_data=['step_error_message'],
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # Customize layout for polish
    fig.update_layout(
        xaxis_title="Instance Name",
        yaxis_title="Percent of Status Failures",
        legend_title="Instance Name & Scenario ID",
        template="plotly_white",
        font=dict(size=14),
        bargap=0.15,
        bargroupgap=0.1
    )

    # Add text annotations inside bars
    fig.update_traces(textposition="outside")

    # Build the FIG construct to return
    FIG = structures.get("plotly")
    FIG["title"] = "Percent of Scenario Failures"
    FIG["data"] = fig
    
    return FIG