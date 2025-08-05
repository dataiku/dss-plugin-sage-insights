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