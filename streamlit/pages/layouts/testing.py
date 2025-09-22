import streamlit as st
import random
import pandas as pd
from numpy.random import default_rng as rng


from sage.src import dss_streamlit
from sage.src import dss_funcs
from sage.src import dss_folder
from sage.dashboards.data_structures import display_graph


# ------------------------------------------------------------------------------------
def main(data_category, display_data, modules):
    df = pd.DataFrame(
        rng(0).standard_normal((12, 5)), columns=["a", "b", "c", "d", "e"]
    )

    event = st.dataframe(
        df,
        key="data",
        on_select="rerun",
        selection_mode=["multi-row", "multi-column"],
    )

    event.selection

    return
    