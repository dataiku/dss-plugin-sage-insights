import pandas as pd
import plotly.express as px
from sage.src import dss_streamlit
from sage.insights.data_structures import structures


def main(filters = {}):
    # read the base layer data -- Change path for different data
    df = dss_streamlit.filter_base_data("/scenarios/metadata.csv", filters)

    # load data structure
    FIG = structures.get("metric")
    
    # Perform logic here
    filtered_df = df[df["sceanrio_active"] == True]
    FIGS = []
    FIG["label"] = "Total number of Enabeld Scenarios -- All"
    FIG["data"] = filtered_df["scenario_id"].count()
    FIGS.append(FIG)

    # Split by Instance
    for i, g in filtered_df.groupby("instance_name"):
        FIG = structures.get("metric")
        FIG["label"] = f"Total number of Enabled Scenarios -- {i}"
        FIG["data"] = g["scenario_id"].count()
        FIGS.append(FIG)

    return FIGS