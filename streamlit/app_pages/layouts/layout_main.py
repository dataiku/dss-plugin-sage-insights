import streamlit as st
import pandas as pd
import tomllib
from sage.src import dss_folder
from sage.streamlit.app_pages.layouts import layout_glance
from sage.streamlit.app_pages.layouts import layout_filter
from sage.streamlit.app_pages.layouts import layout_custom


def main(category, dss_objects):
    # Load base metdata df
    data_category = category.lower()
    data_category = data_category.replace(" ", "_")
    try:
        df = dss_folder.read_folder_input(
            folder_name = "base_data",
            path = f"/{st.session_state.instance_name}/{data_category}/metadata.csv"
        )
    except:
        df = pd.DataFrame()
    
    # load toml config
    with open(".streamlit/sage_config.toml", "rb") as f:
        config_data = tomllib.load(f)
    try:
        config = config_data[data_category]
    except:
        config = {}
    
    # initialize the module
    st.title(f"{category} Metadata")
    tab1, tab2, tab3, tab4 = st.tabs(["About", "At a glance", "Drill Down", "Custom Metrics & Graphs"])
    with tab1:
        about = config.get("about", "#### No information found.")
        st.markdown(about)
    with tab2:
        if (dss_objects and not df.empty):
            layout_glance.body(category, dss_objects, df, config)
        else:
            st.error("No Insights Found!!")
    with tab3:
        if not df.empty:
            layout_filter.body(category, dss_objects, df, config)
        else:
            st.error("No Metadata Found!!")
    with tab4:
        layout_custom.body(category, dss_objects, df, config)
        