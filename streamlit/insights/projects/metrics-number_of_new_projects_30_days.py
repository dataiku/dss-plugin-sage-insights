import streamlit as st
import pandas as pd
import plotly.express as px

from sage.insights.data_structures import structures
from sage.src import dss_funcs, dss_folder
from datetime import date, timedelta

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
    count = len(df[df["creationOn"].dt.date >= (date.today() - timedelta(30))]["project_key"])
    # Perform logic here
    FIGS = []
    FIG["label"] = "Total new projects last 30 days -- All"
    FIG["data"] = len(df[df["creationOn"].dt.date >= (date.today() - timedelta(30))]["project_key"])
    FIGS.append(FIG)

    # Split by Instance
    for i, g in df.groupby("instance_name"):
        FIG = structures.get("metric")
        FIG["label"] = f"Total new projects last 30 days -- {i}"
        recent_projects = g[g["creationOn"].dt.date >= (date.today() - timedelta(30))]
        FIG["data"] = recent_projects["project_key"].nunique()
        FIGS.append(FIG)

    return FIGS
