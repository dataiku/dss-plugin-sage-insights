import streamlit as st
import pandas as pd
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
        st.write("Found custom modules")
        tmp_display_data, tmp_d = collect_display_data(display_type, custom_dss_objects)
        display_data += tmp_display_data
        d = d | tmp_d

    # -------------------------------------------------------------------------
    # Display
    if not display_data:
        st.error(f"No {display_type} to display.")
        return

    if display_type == "Future Metrics Layout":
        st.write()
        #items_per_row = 3
        #for i in range(0, len(display_data), items_per_row):
        #    row_items = display_data[i : i + items_per_row]
        #    cols = st.columns(len(row_items))
        #    for j, item in enumerate(row_items):
        #        with cols[j]:
        #            module_name = d[key][0]
        #            fp = d[key][1]
        #            data = dss_funcs.load_insights(module_name, fp)
        #            display_graph.main(data)
    elif display_type == "metrics":
        for key in display_data:
            with st.container(border=True):
                module_name = d[key][0]
                fp = d[key][1]
                data = dss_funcs.load_insights(module_name, fp)
                display_graph.main(data)
    elif display_type == "graphs":
        for key in display_data:
            with st.container(border=True):
                module_name = d[key][0]
                fp = d[key][1]
                data = dss_funcs.load_insights(module_name, fp)
                display_graph.main(data)