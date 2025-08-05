import pandas as pd
import plotly.express as px
from sage.src import dss_streamlit
from sage.insights.data_structures import structures


def main(filters = {}):
    # read the base layer data -- Change path for different data
    df = dss_streamlit.filter_base_data("/users/metadata.csv", filters)

    # Perform logic here
    from datetime import date, timedelta
    FIG = structures.get("metric")

    # Perform logic here
    FIGS = []
    FIG["label"] = "New Users over the last 30 days -- All"
    FIG["data"] = df[df["creationDate"].dt.date >= (date.today() - timedelta(30))]["login"].nunique()
    FIGS.append(FIG)

    # Split by Instance
    for i, g in df.groupby("instance_name"):
        FIG = structures.get("metric")
        FIG["label"] = f"New Users over the last 30 days -- {i}"
        FIG["data"] = g[g["creationDate"].dt.date >= (date.today() - timedelta(30))]["login"].nunique()
        FIGS.append(FIG)

    return FIGS