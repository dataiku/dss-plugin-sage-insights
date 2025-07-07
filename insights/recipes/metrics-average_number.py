import streamlit as st
import pandas as pd
from sage.src import dss_folder
from sage.insights.data_structures import structures

def main(df=pd.DataFrame()):
    # load data structure
    fig = structures.get("metric")

    # Load additional data
    if df.empty:
        df = dss_folder.read_folder_input(
            folder_name="base_data",
            path=f"/recipes/metadata.csv" # change this line
        )

    # Perform logic here

    # Set values
    fig["label"] = "Average number of Recipes per Project"
    fig["data"] = round(df.groupby("project_key")["recipe_name"].size().mean(), 0)

    return fig