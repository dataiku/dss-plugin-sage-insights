import streamlit as st
import pandas as pd
import plotly.express as px

from sage.insights.data_structures import structures
from sage.src import dss_funcs, dss_folder

local_client = dss_funcs.build_local_client()
project_handle = local_client.get_default_project()
sage_project_key = project_handle.project_key

def main(df=pd.DataFrame()):
    # load data structure
    data = structures.get("metric")

    # Load additional data
    if df.empty:
        df = dss_folder.read_local_folder_input(
            sage_project_key = sage_project_key,
            project_handle = project_handle,
            folder_name="base_data",
            path=f"/projects/metadata.csv" # change this line
        )

    # Perform logic here
    from datetime import date, timedelta

    # Set values
    data["label"] = "Total new projects last 30 days"
    data["data"] = len(df[df["creationOn"].dt.date >= (date.today() - timedelta(30))]["project_key"])

    return data