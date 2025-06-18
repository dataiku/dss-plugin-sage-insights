import streamlit as st
from sage.streamlit.pages.layouts import layout_basic, layout_filter, layout_custom

def main(category, data_category, dss_objects, df, config):
    st.title(f"{category} Metadata")
    tab1, tab2, tab3, tab4 = st.tabs(["About", "At a glance", "Drill Down", "Custom Metrics & Graphs"])
    with tab1:
        st.markdown(config["about"])
    with tab2:
        if dss_objects:
            layout_basic.body(category, dss_objects, df)
        else:
            st.error("No Insights Found!!")
    with tab3:
        layout_filter.main(data_category, df, config)
    with tab4:
        layout_custom.main(category)