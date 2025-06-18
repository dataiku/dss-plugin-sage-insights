import streamlit as st
import pandas as pd

from sage.streamlit.pages.layouts import layout_basic, layout_custom
from sage.src import dss_funcs, dss_folder
try:
    from sage.insights import users as dss_objects # change this line
except:
    dss_objects = False

# -----------------------------------------------------------------------------
# Display the metrics of metadata layer
category = "Users"
st.title(f"{category} Metadata")
tab1, tab2 = st.tabs(["At a glance", "Custom Metrics & Graphs"])
with tab1:
    # Load data
    data_category = category.lower()
    df = dss_folder.read_folder_input(
        folder_name = "base_data",
        path = f"/instance/_dataiku_{data_category}.csv",
        data_type = "DF"
    )
    if dss_objects:
        # Load Body
        layout_basic.body(category, dss_objects, df)
    else:
        st.error("No Insights Found!!")
        st.dataframe(df)
with tab2:
    layout_custom.main(category)
