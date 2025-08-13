import pandas as pd
import plotly.express as px
from sage.src import dss_streamlit
from sage.insights.data_structures import structures


def main(filters = {}):
    # read the base layer data -- Change path for different data
    df = dss_streamlit.filter_base_data("/recipes/metadata.csv", filters)

    # Perform logic here

    # Set values
    fig = structures.get("metric")
    fig["label"] = "Total number of Recipes"
    fig["data"] = df["recipe_name"].nunique()

    # load data structure
    FIG = structures.get("metric")
    
    # Perform logic here
    FIGS = []
    FIG["label"] = "Total number of Recipes -- All"
    FIG["data"] = df["recipe_name"].nunique()
    FIGS.append(FIG)

    # Split by Instance
    for i, g in df.groupby("instance_name"):
        FIG = structures.get("metric")
        FIG["label"] = f"Total number of Recipes -- {i}"
        FIG["data"] = g["recipe_name"].nunique()
        FIGS.append(FIG)

    return FIGS