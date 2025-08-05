import streamlit as st
import pandas as pd
import random

from sage.src import dss_funcs
from sage.insights.data_structures import display_graph


# ------------------------------------------------------------------------------------
def main(data_category, display_data, modules, filters):
    # Enable Filtering
    with st.sidebar:
        with st.container(border=True):
            final_filter = filters
            for key in filters:
                final_filter[key] = st.multiselect(filters[key]["label"], filters[key]["values"])

    # load only the metric insights
    insights = []
    for value in display_data:
        if value.split(" ")[0].lower() == "graphs":
            insights.append(value)
    if not insights:
        st.error(f"No {data_category} Graphs to display.")
        return

    # Display
    st.markdown("**Caution** - Utilizing certain filters may void/zero-out a graph.")
    random_integers = []
    for key in insights:
        with st.container(border=True):
            module_name = modules[key][0]
            fp = modules[key][1]
            FIG = dss_funcs.load_insights(module_name, fp, final_filter)
            if "key" in FIG:
                while True:
                    random_integer = random.randint(1, 10000)
                    if random_integer not in random_integers:
                        random_integers.append(random_integer)
                        break # break the loop, this is intended
                FIG["key"] = FIG["key"] + f"_display.{random_integer}"
            display_graph.main(FIG)
    
    return