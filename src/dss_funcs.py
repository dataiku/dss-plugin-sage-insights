import dataiku
import os
import importlib
import re
import pandas as pd

from sage.src import dss_folder

# -----------------------------------------------------------------------------
def get_dss_name(client):
    instance_info = client.get_instance_info()
    instance_name = instance_info.node_name.lower()
    instance_name = re.sub(r'[^a-zA-Z0-9]', ' ', instance_name)
    instance_name = re.sub(r'\s+', '_', instance_name)
    return instance_name

def get_nested_value(data, keys):
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return False
    return current


def collect_modules(module):
    import streamlit as st
    d = {}
    directory = module.__path__[0]
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(".py") and f != "__init__.py":
                module_name = f[:-3]
                path = root.replace(directory, "")
                fp = os.path.join(root, f)
                delimiters = r'[-_]'
                words = re.split(delimiters, module_name)
                capitalized_words = [word.capitalize() for word in words]
                final_string = " ".join(capitalized_words)
                d[final_string] = [module_name, fp]
    return d


def load_module(module_name, fp, df_filter={}):
    spec = importlib.util.spec_from_file_location(module_name, fp)
    try:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, 'main'):
            results = module.main(df, df_filter)
    except Exception as e:
        results = [False, f"Error importing or running ({fp}) {module_name}: {e}"]
        return results
    return results


def load_insights(module_name, fp, df_filter=pd.DataFrame()):
    results = {}
    spec = importlib.util.spec_from_file_location(module_name, fp)
    try:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, 'main'):
            results = module.main(df_filter)
    except Exception as e:
        import streamlit as st
        st.error(f"Error importing or running ({fp}) {module_name}: {e}")
        results = {}
        return results
    return results


def get_dss_commits():
    client = dataiku.api_client()
    project_handle = client.get_project(dataiku.default_project_key())
    dataset = project_handle.get_dataset("dss_commits")
    if not dataset.exists():
        dataset = project_handle.create_dataset(
            dataset_name = "dss_commits",
            type = "StatsDB",
            params = {
                'view': 'COMMITS',
                'orderByDate': False,
                'clusterTasks': {},
                'commits': {},
                'jobs': {},
                'scenarioRuns': {},
                'flowActions': {}
            }
        )
        schema = {
            "columns": [
                {"name": "project_key", "type": "string"},
                {"name": "commit_id", "type": "string"},
                {"name": "author", "type": "string"},
                {"name": "timestamp", "type": "bigint"},
                {"name": "added_files", "type": "int"},
                {"name": "added_lines", "type": "int"},
                {"name": "removed_files", "type": "int"},
                {"name": "removed_lines", "type": "int"},
                {"name": "changed_files", "type": "int"},
            ],
            "userModified": True,
        }
        r = dataset.set_schema(schema=schema)
    return dataset

def stack_partition_data():
    # create a partitioned folder dataframe
    folder = dss_folder.get_folder(folder_name="partitioned_data")
    partitions = folder.list_partitions()
    folder_df = pd.DataFrame(partitions, columns=["partitions"])
    cols = ["instance_name", "category", "module", "dt"]
    folder_df[cols] = folder_df["partitions"].str.split("|", expand=True)

    # get latest partition
    max_date = folder_df['dt'].max()
    filtered_df = folder_df[folder_df['dt'] == max_date]

    # Loop over the sets and gather
    groups = filtered_df.groupby(by=["category", "module"])
    for i, g in groups:
        category, module = i
        # loop over and build consolidated df
        df = pd.DataFrame()
        for partition in g["partitions"].tolist():
            path = folder.list_paths_in_partition(partition=partition)[0]
            tdf = dss_folder.read_folder_input(folder_name="partitioned_data", path=path)
            if df.empty:
                df = tdf
            else:
                df = pd.concat([df, tdf], ignore_index=True)
        # Write consolidated DF to folder
        dss_folder.write_folder_output(
            folder_name = "base_data",
            path = f"/{category}/{module}.csv",
            data_type = "DF",
            data = df
        )
    return