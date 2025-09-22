import streamlit as st
import random

from sage.src import dss_streamlit
from sage.src import dss_funcs
from sage.src import dss_folder
from sage.dashboards.data_structures import display_graph


# ------------------------------------------------------------------------------------
def main(data_category, display_data, modules):
    with st.sidebar:
        with st.container(border=True):
            # Select the Dataset
            datasets = dss_streamlit.get_datasets(data_category)
            dataset = st.selectbox(
                label = "Select a DataFrame",
                options = datasets,
                index = 0
            )

            # Load the df
            import dataiku
            df = dss_folder.read_local_folder_input(
                sage_project_key = dataiku.default_project_key(),
                project_handle = dataiku.api_client().get_default_project(),
                folder_name = "base_data",
                path = f"/{data_category}/{dataset}.csv"
            )

            # Column Filter (removing / adding columns)
            col_filter = st.checkbox("Add Custom Column Filters", key="col_filter")
            if col_filter:
                col_filters = st.multiselect(f"Select dataframe columns to limit dataframe on", list(df.columns))
                if col_filters:
                    df = df[col_filters]
                    df.drop_duplicates(keep='first', inplace=True, ignore_index=True)

            # Row Filter (removing / adding rows)
            row_filter = st.checkbox("Add Custom Row Filters", key="row_filter")
            if row_filter:
                df = dss_streamlit.filter_dataframe(df)


    # Display
    st.dataframe(df)
    return