import dataiku
import os
import importlib
import re
import pandas as pd
import tomllib


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


def stack_partition_data():
    # create a partitioned folder dataframe
    folder = dss_folder.get_folder(folder_name="partitioned_data")
    partitions = folder.list_partitions()
    folder_df = pd.DataFrame(partitions, columns=["partitions"])
    cols = ["instance_name", "category", "module", "dt"]
    folder_df[cols] = folder_df["partitions"].str.split("|", expand=True)

    # get latest partition
    max_date = folder_df['dt'].max()
    dss_folder.write_folder_output(
        folder_name = "base_data",
        path = f"/partition.csv",
        data_type = "DF",
        data = pd.DataFrame([max_date], columns=["latest_partition"])
    )
    filtered_df = folder_df[folder_df['dt'] == max_date]

    # Loop over the sets and gather
    groups = filtered_df.groupby(by=["category", "module"])
    for i, g in groups:
        category, module = i
        # loop over and build consolidated df
        df = pd.DataFrame()
        for partition in g["partitions"].tolist():
            paths = folder.list_paths_in_partition(partition=partition)
            for path in paths:
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


def get_custom_config(path):
    client = dataiku.api_client()
    project_handle = client.get_default_project()
    library = project_handle.get_library()
    try:
        file = library.get_file(path=path)
        config_data = tomllib.loads(file.read())
    except:
        config_data = {}
    return config_data


def collect_display_data(load_modules):
    display_data = []
    modules = collect_modules(load_modules)
    for key in modules.keys():
        r_type = key.split(" ")
        r_type = r_type[0].lower()
        display_data.append(key)
    return modules, display_data


if __name__ == "__main__":
    main()