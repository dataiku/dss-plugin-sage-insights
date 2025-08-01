import streamlit as st
import pandas as pd
import plotly.express as px

from sage.insights.data_structures import structures
from sage.src import dss_funcs, dss_folder

local_client = dss_funcs.build_local_client()
project_handle = local_client.get_default_project()
sage_project_key = project_handle.project_key

def main(df=pd.DataFrame()):

    # Load additional data
    if df.empty:
        df = dss_folder.read_local_folder_input(
            sage_project_key = sage_project_key,
            project_handle = project_handle,
            folder_name="base_data",
            path=f"/projects/metadata.csv" # change this line
        )

    # load data structure
    FIG = structures.get("metric")
    
    # Perform logic here
    FIGS = []
    FIG["label"] = "Total number of Tutorial Projects -- All"
    FIG["data"] = df['tags'].apply(lambda x: 'tutorial' in x).sum()
    FIGS.append(FIG)

    # Split by Instance
    for i, g in df.groupby("instance_name"):
        FIG = structures.get("metric")
        FIG["label"] = f"Total number of Tutorial Projects -- {i}"
        FIG["data"] = g['tags'].apply(lambda x: 'tutorial' in x).sum()
        FIGS.append(FIG)

    return FIGS
