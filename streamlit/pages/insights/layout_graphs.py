import streamlit as st
import pandas as pd
import random

from sage.src import dss_funcs
from sage.src import dss_folder
from sage.insights.data_structures import display_graph

filter_df = dss_folder.read_base_data("/metadata_primary_keys.csv")
if "filter_df" not in st.session_state:
    st.session_state.filter_df = filter_df



# ------------------------------------------------------------------------------------
def main(data_category, display_data, modules):
    # Enable Filtering
    with st.sidebar:
        with st.container(border=True):
            # Build the filters dictionary
            st_filters = {}
            final_filter = {}
            st_filters["instance_name"] = {"label": "Instance Name",       "options": filter_df["instance_name"].unique().tolist()}
            st_filters["userProfile"]   = {"label": "User Profile Type",   "options": filter_df["userProfile"].unique().tolist()}
            st_filters["enabled"]       = {"label": "User Enablment",      "options": filter_df["enabled"].unique().tolist()}
            st_filters["login"]         = {"label": "User Login Name",     "options": filter_df["login"].unique().tolist()}
            st_filters["project_key"]   = {"label": "Dataiku Project key", "options": filter_df["project_key"].unique().tolist()}
            for key in st_filters:
                label = st_filters[key]["label"]
                options = st_filters[key]["options"]
                final_filter[key] = st.multiselect(label=label, options=options)

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