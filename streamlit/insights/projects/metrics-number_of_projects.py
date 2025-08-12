import pandas as pd
import plotly.express as px
from sage.src import dss_streamlit
from sage.insights.data_structures import structures


def main(filters = {}):
    # read the base layer data -- Change path for different data
    df = dss_streamlit.filter_base_data("/projects/metadata.csv", filters)

    # Perform logic here

    # Set values
    data = structures.get("metric")
    data["label"] = "Total DSS Projects"
    data["data"] = df["project_key"].nunique()

    return data