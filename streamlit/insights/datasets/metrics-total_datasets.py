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
            path=f"/datasets/metadata.csv"
        )

    # load data structure
    FIG = structures.get("metric")

    FIGS = []
    FIG["label"] = "Average number of Datasets per Project -- All"
    FIG["data"] = int(round(df.groupby("project_key")["dataset_name"].size().mean(), 0))
    FIGS.append(FIG)

    # Split by Instance
    for i, g in df.groupby("instance_name"):
        FIG = structures.get("metric")
        FIG["label"] = f"Average number of Datasets per Project -- {i}"
        FIG["data"] = int(round(g.groupby("project_key")["dataset_name"].size().mean(), 0))
        FIGS.append(FIG)

    return FIGS