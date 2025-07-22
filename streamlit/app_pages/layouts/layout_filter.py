import streamlit as st
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import random

from sage.src import dss_funcs
from sage.src import dss_folder
from sage.insights.data_structures import display_graph

local_client = dss_funcs.build_local_client()
project_handle = local_client.get_default_project()
sage_project_key = project_handle.project_key

def filter_columns(df):
    # Add a filtering block
    modify = st.checkbox("Add Custom Column Filters", key="col_filter")
    if not modify:
        return df, []
    df = df.copy()
    columns = list(df.columns)
    options = st.multiselect(f"Select dataframe columns to limit dataframe on", columns)
    filter = options
    if options:
        df = df[filter]
    df.drop_duplicates(keep='first', inplace=True, ignore_index=True)
    return df, filter


def filter_dataframe(df, filter=[]):
    # Add a filtering block
    modify = st.checkbox("Add Custom Row Filters", key="row_filter")
    if not modify:
        return df
    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass
        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)
    
    # Fix empty filter
    if not filter:
        filter = df.columns

    # Build container
    to_filter_columns = st.multiselect("Filter dataframe rows on", filter)
    for column in to_filter_columns:
        left, right = st.columns((1, 20))
        left.write("↳")
        # Treat columns with < 10 unique values as categorical
        if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
            user_cat_input = right.multiselect(
                f"Values for {column}",
                df[column].unique(),
                default=list(df[column].unique()),
            )
            df = df[df[column].isin(user_cat_input)]
        elif is_numeric_dtype(df[column]):
            _min = float(df[column].min())
            _max = float(df[column].max())
            step = (_max - _min) / 100
            user_num_input = right.slider(
                f"Values for {column}",
                _min,
                _max,
                (_min, _max),
                step=step,
            )
            df = df[df[column].between(*user_num_input)]
        elif is_datetime64_any_dtype(df[column]):
            user_date_input = right.date_input(
                f"Values for {column}",
                value=(
                    df[column].min(),
                    df[column].max(),
                ),
            )
            if len(user_date_input) == 2:
                user_date_input = tuple(map(pd.to_datetime, user_date_input))
                start_date, end_date = user_date_input
                df = df.loc[df[column].between(start_date, end_date)]
        else:
            user_text_input = right.text_input(
                f"Substring or regex in {column}",
            )
            if user_text_input:
                df = df[df[column].str.contains(user_text_input)]

    return df


def uncheck_checkbox():
    st.session_state.checkbox_state = False
    return


def body(data_category, modules, display_data):
    with st.container():
        # Select a Dataset
        datasets = []
        folder = dss_folder.get_folder(
            sage_project_key=sage_project_key, project_handle=project_handle, folder_name="base_data"
        )
        for p in folder.list_paths_in_partition():
            if data_category in p:
                csv = p.split("/")[-1].replace(".csv", "")
                datasets.append(csv)
        dataset = st.selectbox("Which dataset would you like to review?", datasets)
        # Every form must have a submit button.
        if 'checkbox_state' not in st.session_state:
            st.session_state.checkbox_state = False
        st.checkbox(f"Load DataFrame", key='checkbox_state', value=st.session_state.checkbox_state)
        
    # -------------------------------------------------------------------------
    # Display Form inputs
    if st.session_state.checkbox_state:
        with st.container(border=True):
            # Clear display button
            st.button("Clear Display", on_click=uncheck_checkbox)
            
            # Load the df
            df = dss_folder.read_local_folder_input(
                sage_project_key = sage_project_key,
                project_handle = project_handle,
                folder_name = "base_data",
                path = f"/{data_category}/{dataset}.csv"
            )

            # Filter the metadata df columns for what they are initially interested in
            df, filter = filter_columns(df)
            df = filter_dataframe(df, filter)

            # Check box which added graph you want
            load_custom = st.checkbox("Load Custom Graphs/Charts", key="custom_graphs_charts")
            if load_custom:
                display_data_options = st.multiselect( "Select an added graph/chart to display", display_data)
                if display_data_options:
                    for key in display_data_options:
                        module_name = modules[key][0]
                        fp = modules[key][1]
                        FIG = dss_funcs.load_insights(module_name, fp, df)
                        if isinstance(FIG, dict) and "pass" in FIG and FIG["pass"]:
                            if "key" in FIG:
                                random_integer = random.randint(1, 10)
                                FIG["key"] = FIG["key"] + f"_display.{random_integer}"
                            display_graph.main(FIG)
            else:
                # Display the DF
                st.dataframe(df)
