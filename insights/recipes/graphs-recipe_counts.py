import streamlit as st
import pandas as pd
from sage.src import dss_folder
from sage.insights.data_structures import structures

def main(df=pd.DataFrame()):
    # load data structure
    data = structures.get("bar_chart") # change this line

    # Load additional data
    if df.empty:
        df = dss_folder.read_folder_input(
            folder_name="base_data",
            path=f"/{st.session_state.instance_name}/recipes/metadata.csv" # change this line
        )

    # Perform logic here
    df = df.groupby("recipe_type")["project_key"].count()
    #df = df.reset_index()

    # Build the data structure
    data["title"] = "Recipes count by Recipe Type"
    data["data"] = df
    data["x_label"] = "Count of Recipe Types"
    data["y_label"] = "Recipe Type"
    data["horizontal"] = True
    
    return data