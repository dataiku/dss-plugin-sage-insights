import dataiku
import os
import duckdb
import warnings
import pandas as pd
import streamlit as st


duckdb_home = "/tmp/sage"
duckdb_name = f"{duckdb_home}/sage.duckdb"

folder = dataiku.Folder(
    lookup="base_data",
    project_key=dataiku.default_project_key(),
    ignore_flow=True
)


def create_duckdb():
    # Test that directory path works
    try:
        os.makedirs(duckdb_home, exist_ok=True)
    except OSError as e:
        return [False, e]
    # Connect to DB
    try:
        con = duckdb.connect(duckdb_name)
        con.close()
    except Exception as e:
        return [False, e]
    return


def function_with_warning(df):
    for c in df.columns:
        if df[c].dtype == "object":
            temp_col = pd.to_datetime(df[c],  errors='coerce')
            if temp_col.notna().all():
                df[c] = temp_col
                min_date = df[df[c] != "1970-01-01"][c].min()
                df.loc[df[c] == "1970-01-01", c] = min_date
    return df


def load_duckdb():
    con = duckdb.connect(duckdb_name)
    csvs = folder.list_paths_in_partition()
    for csv in csvs:
        # Read initial csv
        try:
            with folder.get_download_stream(path=csv) as reader:
                df = pd.read_csv(reader)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                df = function_with_warning(df)
        except Exception as e:
            return [False, e]

        # Save to Docker Image, delete memory space
        try:
            csv = csv[1:]
            csv = csv.replace("/", "_")
            df.to_csv(f"{duckdb_home}/{csv}", index=False)
            del df
        except Exception as e:
            return [False, e]

        # load to duckdb
        try:
            table_name = csv.replace(".csv", "")
            con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_csv_auto('{duckdb_home}/{csv}')")
        except Exception as e:
            return [False, e]
    con.close()
    return


def initialize_duckdb(force=False):
    if not os.path.exists(duckdb_name) or force == True:
        create_duckdb()
        progress_text = "Loading Sage data in progress. Please wait......"
        my_bar = st.progress(0, text=progress_text)
        load_duckdb()
        my_bar.empty()
        st.success("Sage data loaded Successful!!")
        st.session_state.initialize = False
    return


def query_duckdb(query):
    con = duckdb.connect(duckdb_name)
    df = con.execute(query).df()
    con.close()
    return df