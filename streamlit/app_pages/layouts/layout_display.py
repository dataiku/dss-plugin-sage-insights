import streamlit as st
import pandas as pd
import random

from sage.src import dss_funcs
from sage.insights.data_structures import display_graph


def body(display_type, modules, display_data):
    # Quick check that this display type is valid and found
    if not display_data:
        st.error(f"No {display_type} to display.")
        return

    insights = []
    for value in display_data:
        if value.split(" ")[0].lower() == display_type:
            insights.append(value)

    if not insights:
        st.error(f"No {display_type} to display.")
        return

    # Display Metrics TAB
    if display_type == "metrics":
        for key in insights:
            with st.container(border=True):
                module_name = modules[key][0]
                fp = modules[key][1]
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
        for key in insights:
            with st.container(border=True):
                module_name = modules[key][0]
                fp = modules[key][1]
                FIG = dss_funcs.load_insights(module_name, fp)
                if "key" in FIG:
                    random_integer = random.randint(1, 10)
                    FIG["key"] = FIG["key"] + f"_display.{random_integer}"
                display_graph.main(FIG)