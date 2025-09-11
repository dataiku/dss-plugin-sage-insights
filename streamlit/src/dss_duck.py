import dataiku
import os
import duckdb
import sqlparse
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
    total_csvs = len(csvs)
    progress_text = "Loading Sage data in progress. Please wait......"
    progress_bar = st.progress(0, text=progress_text)
    status_text = st.empty()
    for i, csv in enumerate(csvs, start=1):
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
        # Update progress bar + status text
        progress = int(i / total_csvs * 100)
        progress_bar.progress(progress, text=progress_text)
        status_text.text(f"Processed {i}/{total_csvs} base data 'csvs' ({csv})")
    # Close Connection and Report
    con.close()
    st.success("Sage data loaded Successful!!")
    return


def initialize_duckdb(force=False):
    if not os.path.exists(duckdb_name) or force == True:
        create_duckdb()
        load_duckdb()
        st.session_state.initialize = False
    return


def filters_conversion(filters):
    final_filter = []
    for filter in filters.keys():
        if not filters[filter]:
            continue
        if filter == "enabled":
            if len(filters[filter]) != 1:
                continue
            b = str(filters["enabled"][0]).upper()
            s = f"mpk.{filter} = {b}"
            final_filter.append(s)
        else:
            s = f"mpk.{filter} IN ("
            in_clause = ", ".join(f"'{x}'" for x in filters[filter])
            s += f"{in_clause})"
            final_filter.append(s)
    return final_filter


def build_sql(query: dict, filters: dict) -> str:
    # SELECT
    select_clause = "SELECT " + ", ".join(query.get("select", ["*"]))
    # FROM
    from_clause = "FROM " + ", ".join(query.get("from", []))
    # JOIN
    join_clause = ""
    if query.get("join"):
        join_clause = "\n" + "\n".join(query["join"])
    # WHERE
    filter_clause = ""
    if filters and "_metadata" in from_clause:
        filter_clause = "LEFT JOIN metadata_primary_keys AS mpk ON ("
        for tbl in query["from"]:
            if "AS" in tbl.upper():
                tbl = tbl.split(" ")
                tbl = tbl[-1]
            if "user_metadata" in tbl.lower():
                filter_clause += f"{tbl}.instance_name = mpk.instance_name"
            else:
                filter_clause += f"{tbl}.instance_name = mpk.instance_name AND {tbl}.project_key = mpk.project_key"
        filter_clause += ")"
        filters = filters_conversion(filters)
        query["where"] += filters
    where_clause = ""
    if query.get("where"):
        where_clause = "\nWHERE " + " AND ".join(query["where"])
    # GROUP BY
    group_clause = ""
    if query.get("group"):
        group_clause = "\nGROUP BY " + ", ".join(query["group"])
    # ORDER BY
    order_clause = ""
    if query.get("order"):
        order_clause = "\nORDER BY " + ", ".join(query["order"])
    # Put it all together
    sql = "\n".join([select_clause, from_clause, join_clause, filter_clause, where_clause, group_clause, order_clause])
    sql = sqlparse.format(sql, reindent=True, keyword_case='upper')
    return sql


def query_duckdb(query, filters = {}, debug=False):
    sql_query = build_sql(query, filters)
    if debug:
        import streamlit as st
        st.write(sql_query)
    # Connect to the database, query, return results
    try:
        con = duckdb.connect(duckdb_name, read_only=True)
        df = con.execute(sql_query).df()
        con.close()
    except Exception as e:
        raise Exception(e)
    return df