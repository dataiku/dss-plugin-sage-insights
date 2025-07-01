import streamlit as st
import pandas as pd
import tomllib
from sage.src import dss_folder, dss_funcs
from sage.streamlit.app_pages.layouts import layout_display
from sage.streamlit.app_pages.layouts import layout_filter


def main(category, dss_objects, custom_dss_objects):
    # load toml config
    data_category = category.lower()
    data_category = data_category.replace(" ", "_")
    with open(".streamlit/sage_config.toml", "rb") as f:
        config_data = tomllib.load(f)
    try:
        config = config_data[data_category]
    except:
        config = {}
    
    # initialize the module
    st.title(f"{category} Metadata")
    tab1, tab2, tab3, tab4 = st.tabs(["About", "Metrics", "Charts & Graphs", "Explore the Data"])
    with tab1:
        about = config.get("about", "#### No information found.")
        st.markdown(about)
    with tab2:
        layout_display.body("metrics", dss_objects, custom_dss_objects)
    with tab3:
        layout_display.body("graphs", dss_objects, custom_dss_objects)
    with tab4:
        layout_filter.body(data_category, config, "filters", dss_objects, custom_dss_objects)
        