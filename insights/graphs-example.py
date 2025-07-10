import streamlit as st
import pandas as pd
from sage.src import dss_folder
from sage.insights.data_structures import structures

def main(df=pd.DataFrame()):
    # load data structure
    data = structures.get("bar_chart") # change this line
    #st.write(data)

    # Load additional data
    if df.empty:
        df = dss_folder.read_folder_input(
            folder_name="base_data",
            path=f"/CATEGORYDATAFRAME.csv" # change this line
        )

    # Perform logic here
    df = df

    # Build the data structure
    data["title"] = "Example_Title"
    data["data"] = df
    
    return data