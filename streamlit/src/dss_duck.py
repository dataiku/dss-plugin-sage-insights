import dataiku
import duckdb
import pandas as pd
import streamlit as st
import sqlparse
import os
import io
import shutil
import importlib
import time
import logging
logger = logging.getLogger(__name__)

from sage.src import dss_sage_tbls


duckdb_home = "/tmp/sage"
duckdb_name = f"{duckdb_home}/sage.duckdb"

folder = dataiku.Folder(
    lookup="base_data",
    project_key=dataiku.default_project_key(),
    ignore_flow=True
)

# -----------------------------------------------------------------------------
# CREATE DUCKDB
def create_duckdb():
    if os.path.exists(duckdb_home):
        shutil.rmtree(duckdb_home)
    try:
        os.makedirs(duckdb_home, exist_ok=True)
    except OSError as e:
        logger.error(e)
    try:
        con = duckdb.connect(duckdb_name)
        con.close()
    except Exception as e:
        logger.error(e)
    return


def initialize_duckdb(force=False):
    if not os.path.exists(duckdb_name) or force == True:
        progress_text = "Setting up Sage Database. Please wait......"
        progress_bar = st.progress(0, text=progress_text)
        status_text = st.empty()
        funcs = [create_duckdb, import_base_data, create_additional_tables]
        total_funcs = len(funcs)
        for i, func in enumerate(funcs, start=1):
            func()
            progress = int(i / total_funcs * 100)
            progress_bar.progress(progress, text=progress_text)
            status_text.text(f"Completed step {i}/{total_funcs}")
        st.success("Sage data loaded Successful!!")
        st.session_state.initialize = False
    return


# -----------------------------------------------------------------------------
# LOAD DUCKDB
def load_data(filename):
    try:
        table_name = filename.removesuffix(".parquet")
        sql = f"""
            CREATE OR REPLACE TABLE {table_name}
            AS
            SELECT * FROM read_parquet('{duckdb_home}/{filename}')
        """
        with duckdb.connect(duckdb_name) as con:
            con.execute(sql)
    except Exception as e:
        st.error(e)
    return


def import_base_data():
    parquets = folder.list_paths_in_partition()
    total_parquets = len(parquets)
    progress_text = "Copying data into database"
    progress_bar = st.progress(0, text=progress_text)
    status_text = st.empty()
    for i, parquet_path in enumerate(parquets, start=1):
        try:
            with folder.get_download_stream(parquet_path) as stream:
                file_bytes = io.BytesIO(stream.read())
            df = pd.read_parquet(file_bytes)
        except Exception as e:
            logger.error(e)
        try:
            parquet_path = parquet_path[1:]
            parquet_file_name = parquet_path.replace("/", "_")
            df.to_parquet(f"{duckdb_home}/{parquet_file_name}", index=False)
            del df
        except Exception as e:
            logger.error(e)
        load_data(parquet_file_name)
        progress = int(i / total_parquets * 100)
        progress_bar.progress(progress, text=progress_text)
        status_text.text(f"Imported {i}/{total_parquets} base data ({parquet_file_name})")
    time.sleep(1)
    progress_bar.empty()
    status_text.empty()
    return


def create_additional_tables():
    directory = dss_sage_tbls.__path__[0]
    modules = []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(".py") and f != "__init__.py":
                path = root.replace(directory, "")
                fp = os.path.join(root, f)
                modules.append(fp)
    total_modules = len(modules)
    progress_text = "Creating additional Sage Tables"
    progress_bar = st.progress(0, text=progress_text)
    status_text = st.empty()
    for i, module in enumerate(modules, start=1):
        module_name = module.split("/")[-1].removesuffix(".py")
        module_name = f"addon_{module_name}"
        spec = importlib.util.spec_from_file_location(module_name, fp)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        try:
            df = module.main()
        except Exception as e:
            logger.error(e)
        df.to_parquet(f"{duckdb_home}/{module_name}.parquet", index=False)
        del df
        load_data(f"{module_name}.parquet")
        progress = int(i / total_modules * 100)
        progress_bar.progress(progress, text=progress_text)
        status_text.text(f"Created {i}/{total_modules} additional Sage Tables ({module_name})")
    time.sleep(1)
    progress_bar.empty()
    status_text.empty()
    return

# -----------------------------------------------------------------------------
# QUERY DUCKDB
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
        filter_clause = "INNER JOIN metadata_primary_keys AS mpk ON ("
        for og_tbl in query["from"]:
            if "AS" in og_tbl.upper():
                tbl = og_tbl.split(" ")
                tbl = tbl[-1]
            else:
                tbl = og_tbl
            if "users_metadata" in og_tbl.lower():
                filter_clause += f"{tbl}.instance_name = mpk.instance_name AND {tbl}.login = mpk.login"
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
        print(sql_query)
    try:
        con = duckdb.connect(duckdb_name, read_only=True)
        df = con.execute(sql_query).df()
        con.close()
    except Exception as e:
        logger.error(e)
    return df


def query_duckdb_direct(query):
    try:
        con = duckdb.connect(duckdb_name, read_only=True)
        df = con.execute(query).df()
        con.close()
    except Exception as e:
        logger.error(e)
    return df