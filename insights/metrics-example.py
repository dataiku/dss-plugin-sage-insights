import streamlit as st
import pandas as pd
from sage.src import dss_folder
from sage.insights.data_structures import structures

def main(df=pd.DataFrame()):
    # load data structure
    data = structures.get("metric")
    # st.write(data)

    # Load additional data
    df = dss_folder.read_folder_input(
        folder_name="base_data",
        path=f"/CATEGORY/DATAFRAME.csv" # change this line
    )

    # Perform logic here

    # Set values
    data["label"] = "Example_Label"
    data["data"] = 1

    return data