import pandas as pd
import plotly.express as px
from sage.src import dss_streamlit
from sage.insights.data_structures import structures


def main(filters = {}):
    # read the base layer data -- Change path for different data
    df = dss_streamlit.filter_base_data("/datasets/metadata.csv", filters)

    # load data structure
    FIG = structures.get("metric")

    FIGS = []
    FIG["label"] = "Total number of Dataset Names -- All"
    FIG["data"] = df["dataset_name"].count()
    FIGS.append(FIG)

    # Split by Instance
    for i, g in df.groupby("instance_name"):
        FIG = structures.get("metric")
        FIG["label"] = f"Total number of Dataset Names -- {i}"
        FIG["data"] = g["dataset_name"].count()
        FIGS.append(FIG)

    return FIGS