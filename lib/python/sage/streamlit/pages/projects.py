import streamlit as st
import pandas as pd

from sage.src import dss_folder
from sage.src import dss_funcs
try:
    from sage.modules import projects as dss_objects # change this line
except:
    dss_objects = False

# -----------------------------------------------------------------------------
# Set category and load module(s)
category = "Projects"
st.title(f"{category} Metadata")
tab1, tab2 = st.tabs(["Home", "Custom"])
with tab1:
    # Load data
    data_category = category.lower()
    df = dss_folder.read_folder_input(
        folder_name = "base_data",
        path = f"/instance/_dataiku_{data_category}.csv",
        data_type = "DF"
    )
    for c in ["lastModifiedOn", "creationOn"]:
        df[c] = pd.to_datetime(df[c])
    if dss_objects:
        # Load Body
        layout_basic.body(category, dss_objects, df)
    else:
        st.error("No Insights Found!!")
        st.dataframe(df)
with tab2:
    layout_custom.main(category)