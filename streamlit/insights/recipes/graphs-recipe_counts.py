import pandas as pd
import plotly.express as px
from sage.src import dss_streamlit
from sage.insights.data_structures import structures


def main(filters = {}):
    # read the base layer data -- Change path for different data
    df = dss_streamlit.filter_base_data("/recipes/metadata.csv", filters)

    # Perform logic here
    df = df.groupby(["instance_name", "recipe_type"]).size().reset_index(name="count")

    # Plot
    fig = px.bar(
        df,
        y="recipe_type",
        x="count",
        color="instance_name",
        barmode="group",
        text="count",
        labels={"count": "number of recipe types"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # Customize layout for polish
    fig.update_layout(
        yaxis_title="Recipe Type",
        xaxis_title="Count",
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
    FIG["title"] = "Number of Recipes per Instance"
    FIG["data"] = fig
    
    return FIG