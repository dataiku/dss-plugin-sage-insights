from sage.insights.data_structures import structures
from sage.src import dss_duck
import plotly.express as px

def main(filters = {}):
    # Build SQL Query Statement and Query, 
    query = structures.get_query_dict()
    query["select"] = ["base.instance_name", "base.recipe_type", "COUNT(*) AS recipe_count"]
    query["from"]   = ["recipes_metadata as base"]
    query["join"]   = []
    query["where"]  = []
    query["group"]  = ["base.instance_name", "base.recipe_type"]
    query["order"]  = ["base.instance_name", "recipe_count"]
    df = dss_duck.query_duckdb(query, filters, debug=True)

    # Additional Preperation
    df = df.groupby("instance_name").tail(10)
    
    # Plot
    fig = px.bar(
        df,
        y="recipe_type",
        x="recipe_count",
        color="instance_name",
        barmode="group",
        text="recipe_count",
        labels={"recipe_count": "count of recipe type"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # Customize layout for polish
    fig.update_layout(
        yaxis_title="Recipe Type",
        xaxis_title="Total Count",
        legend_title="Instance Name",
        template="plotly_white",
        font=dict(size=14),
        bargap=0.15,
        bargroupgap=0.1
    )

    # Add text annotations inside bars and background lines
    fig.update_traces(textposition="outside")
    fig.update_layout(
        xaxis=dict(showgrid=True, gridcolor='lightgray', zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='lightgray', zeroline=False)
    )

    # Build the FIG construct to return
    FIG = structures.get("plotly")
    FIG["title"] = "Top 10 Recipe Types"
    FIG["data"] = fig
    
    return FIG