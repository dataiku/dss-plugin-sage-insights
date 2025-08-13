import pandas as pd
import plotly.express as px
from sage.src import dss_streamlit
from sage.insights.data_structures import structures


def main(filters = {}):
    # read the base layer data -- Change path for different data
    df = dss_streamlit.filter_base_data("/recipes/metadata.csv", filters)

    # load data structure
    FIG = structures.get("metric")
    
    # Perform logic here
    FIGS = []
    FIG["label"] = "Top Recipe Type -- All"
    filtered_df = df.groupby("recipe_type").size().sort_values(ascending=False).reset_index(name="count")
    recipe = filtered_df["recipe_type"].iloc[0]
    FIG["data"] = recipe
    FIGS.append(FIG)

    # Split by Instance
    for i, g in df.groupby("instance_name"):
        FIG = structures.get("metric")
        FIG["label"] = f"Top Recipe Type -- {i}"
        filtered_df = g.groupby("recipe_type").size().sort_values(ascending=False).reset_index(name="count")
        recipe = filtered_df["recipe_type"].iloc[0]
        FIG["data"] = recipe
        FIGS.append(FIG)

    return FIGS