import pandas as pd
import plotly.express as px
from sage.src import dss_streamlit
from sage.insights.data_structures import structures


def main(filters = {}):
    # read the base layer data -- Change path for different data
    df = dss_streamlit.filter_base_data("/projects/metadata.csv", filters)

    # load data structure
    FIG = structures.get("metric")
    
    # Perform logic here
    FIGS = []
    FIG["label"] = "Total DSS Projects -- All"
    FIG["data"] = df["project_key"].nunique()
    FIGS.append(FIG)

    # Split by Instance
    for i, g in df.groupby("instance_name"):
        FIG = structures.get("metric")
        FIG["label"] = f"Total DSS Projects -- {i}"
        FIG["data"] = g["project_key"].nunique()
        FIGS.append(FIG)

    return FIGS