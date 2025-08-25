from sage.src import dss_duck
from sage.insights.data_structures import structures
import plotly.express as px

def main(filters = {}):
    # Perform logic here
    query = """
        SELECT
            base.instance_name
            , base.recipe_type
            , COUNT(*) as count
        FROM recipes_metadata AS base
        LEFT JOIN metadata_primary_keys AS filter
        ON 
            (base.instance_name = filter.instance_name AND base.project_key = filter.project_key)
        GROUP BY
            base.instance_name,
            base.recipe_type
        ORDER BY base.instance_name, count
    """
    df = dss_duck.query_duckdb(query)
    df = df.groupby("instance_name").tail(10)
    
    # Plot
    fig = px.bar(
        df,
        y="recipe_type",
        x="count",
        color="instance_name",
        barmode="group",
        text="count",
        labels={"count": "count of recipe type"},
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