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

    return fig