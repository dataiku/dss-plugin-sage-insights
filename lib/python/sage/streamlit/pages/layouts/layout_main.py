import streamlit as st
from sage.streamlit.pages.layouts import layout_basic, layout_filter, layout_custom

def main(category, data_category, dss_objects, df):
    st.title(f"{category} Metadata")
    tab1, tab2, tab3 = st.tabs(["At a glance", "Drill Down", "Custom Metrics & Graphs"])
    with tab1:
        if dss_objects:
            layout_basic.body(category, dss_objects, df)
        else:
            st.error("No Insights Found!!")
    with tab2:
        layout_filter.main(data_category, df)
    with tab3:
        layout_custom.main(category)