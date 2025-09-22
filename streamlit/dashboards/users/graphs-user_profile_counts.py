from sage.dashboards.data_structures import structures
from sage.src import dss_duck
import plotly.express as px


def main(filters = {}):
    # Build SQL Query Statement and Query, 
    query = structures.get_query_dict()
    query["select"] = ["*"]
    query["from"]   = ["users_metadata as base"]
    df = dss_duck.query_duckdb(query, filters)

    # Perform logic here
    filtered_df = df[df["enabled"] == True]
    filtered_df = filtered_df.groupby(["instance_name", "userprofile"])["login"].nunique()
    filtered_df = filtered_df.reset_index(name="profile_count")

    # Initial fig
    fig = px.bar(
        filtered_df,
        x="userprofile",
        y="profile_count",
        color="instance_name",
        barmode="group",
        text="profile_count",
        labels={"userprofile": "Dataiku profile", "profile_count": "Cumulative Profile Usage"},
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