import pandas as pd
import plotly.express as px
from sage.src import dss_streamlit
from sage.insights.data_structures import structures


def main(filters = {}):
    # read the base layer data -- Change path for different data
    df = dss_streamlit.filter_base_data("/users/metadata.csv", filters)

    # Perform logic here
    FIG = structures.get("metric")

    FIGS = []
    FIG["label"] = "Total Unique Users -- All"
    total_users = df["login"].nunique()
    enabled_users = int(df.groupby("enabled")["login"].nunique().loc[True])
    delta_users = total_users - enabled_users
    total_users, enabled_users, delta_users
    FIG["data"] = total_users
    FIGS.append(FIG)

    # Split by Instance
    for i, g in df.groupby("instance_name"):
        FIG = structures.get("metric")
        FIG["label"] = f"Total Unique Users -- {i}"
        total_users = g["login"].nunique()
        enabled_users = int(g.groupby("enabled")["login"].nunique().loc[True])
        delta_users = total_users - enabled_users
        total_users, enabled_users, delta_users
        FIG["data"] = total_users
        FIGS.append(FIG)

    return FIGS