import streamlit as st
import pandas as pd
import random

from sage.src import dss_funcs
from sage.insights.data_structures import display_graph


def collect_display_data(display_type, module):
    display_data = []
    d = dss_funcs.collect_modules(module)
    for key in d.keys():
        r_type = key.split(" ")
        r_type = r_type[0].lower()
        if r_type == display_type:
            display_data.append(key)
    return display_data, d


def body(display_type, dss_objects, custom_dss_objects):
    # -------------------------------------------------------------------------
    # Load the INSIGHTS information
    display_data = []
    d = {}
    if dss_objects:
        tmp_display_data, tmp_d = collect_display_data(display_type, dss_objects)
        display_data += tmp_display_data
        d = d | tmp_d
    if custom_dss_objects:
        tmp_display_data, tmp_d = collect_display_data(display_type, custom_dss_objects)
        display_data += tmp_display_data
        d = d | tmp_d

    # -------------------------------------------------------------------------
    # Display
    if not display_data:
        st.error(f"No {display_type} to display.")
        return

    # Display Metrics TAB
    if display_type == "metrics":
        for key in display_data:
            with st.container(border=True):
                module_name = d[key][0]
                fp = d[key][1]
                FIGS = dss_funcs.load_insights(module_name, fp)
                if isinstance(FIGS, list):
                    ncol = len(FIGS)
                    cols = st.columns(ncol, gap="small", border=True)
                    for i in range(ncol):
                        with cols[i]:
                            display_graph.main(FIGS[i])
                else:
                    FIG = FIGS       
                    display_graph.main(FIG)
    
    # Display Graphs TAB                
    elif display_type == "graphs":
        for key in display_data:
            with st.container(border=True):
                module_name = d[key][0]
                fp = d[key][1]
                FIG = dss_funcs.load_insights(module_name, fp)
                if "key" in FIG:
                    random_integer = random.randint(1, 10)
                    FIG["key"] = FIG["key"] + f"_display.{random_integer}"
                display_graph.main(FIG)