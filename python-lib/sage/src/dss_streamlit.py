import streamlit as st
import pandas as pd
from pandas.api.types import ( 
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
    is_bool_dtype,
)

from sage.src import dss_funcs
from sage.src import dss_folder


# ------------------------------------------------------------------------------------
def get_datasets(data_category):
    local_client = dss_funcs.build_local_client()
    project_handle = local_client.get_default_project()
    sage_project_key = project_handle.project_key

    datasets = []
    folder = dss_folder.get_folder(
        sage_project_key=sage_project_key, project_handle=project_handle, folder_name="base_data"
    )
    for p in folder.list_paths_in_partition():
        if data_category in p:
            csv = p.split("/")[-1].replace(".csv", "")
            datasets.append(csv)
    return datasets


def filter_dataframe(df):
    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass
        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)
    # Build container
    filter = df.columns
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


def filter_base_data(path, filters):
    df = dss_folder.read_base_data(path)
    if not filters:
        return df
    
    if "metadata.csv" not in path:
        dot, data_category, file = path.split("/")
        try:
            metadata_df = dss_folder.read_base_data(f"/{data_category}/metadata.csv")
            df = pd.merge(df, metadata_df, how="left", on=["instance_name", "login"])
        except:
            pass

    for column in filters.keys():
        values = filters[column]
        if column not in df.columns or not filters[column]:
            continue
        elif is_categorical_dtype(df[column]) or is_object_dtype(df[column]):
            df = df[df[column].isin(values)]
        elif is_bool_dtype(df[column]):
            if len(values) == 0 or len(values) == 2:
                df = df
            else:
                df = df[df[column] == values[0]]
        else:
            df = df[df[column].str.contains(values)]
    return df