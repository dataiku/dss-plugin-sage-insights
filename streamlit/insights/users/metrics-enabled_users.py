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
            path=f"/users/metadata.csv" # change this line
        )

    # load data structure
    FIG = structures.get("metric")

    # Perform logic here
    FIGS = []
    FIG["label"] = "Enabeld Users -- All"
    FIG["data"] = int(df.groupby("enabled")["login"].nunique().loc[True])
    FIGS.append(FIG)

    # Split by Instance
    for i, g in df.groupby("instance_name"):
        FIG = structures.get("metric")
        FIG["label"] = f"Enabled Users -- {i}"
        FIG["data"] = int(g.groupby("enabled")["login"].nunique().loc[True])
        FIGS.append(FIG)

    return FIGS