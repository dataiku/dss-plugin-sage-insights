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
tab1, tab2 = st.tabs(["Home", "Custom"])
with tab1:
    # Load data
    df = dss_folder.read_folder_input(
        folder_name = "base_data",
        path = f"/instance/_dataiku_users.csv",
        data_type = "DF"
    )
    for c in ["creationDate", "last_session_activity", "first_commit_date", "last_commit_date"]:
        df[c] = pd.to_datetime(df[c])
    if dss_objects:
        # Load Body
        layout_basic.body(category, dss_objects, df)
    else:
        st.error("No Insights Found!!")
        st.dataframe(df)
with tab2:
    layout_custom.main(category)
