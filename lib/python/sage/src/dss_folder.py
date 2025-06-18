# src/helper.py
import dataiku
import pandas as pd
import json
import warnings


client = dataiku.api_client()
project = client.get_default_project()


def get_folder(folder_name):
    folder = dataiku.Folder(
        lookup = folder_name,
        project_key = dataiku.default_project_key(),
        ignore_flow = True
        )
    try:
        folder.get_id()
    except:
        folder = create_folder(folder_name)
    return folder


def create_folder(folder_name):
    # Create Folder
    folder_handle = project.create_managed_folder(
        name = folder_name,
        connection_name = "filesystem_folders"
    )
    # Return Folder object
    folder = dataiku.Folder(
        lookup = folder_name,
        ignore_flow = True,
        project_key = dataiku.default_project_key()
    )
    return folder


def write_folder_output(path, data=None, folder_name="base_data", data_type="DF"):
    folder = get_folder(folder_name)
    if data_type == "DF":
        with folder.get_writer(path) as w:
            w.write(data.to_csv(index=False).encode("utf-8"))
    elif data_type == "JSON":
        with folder.get_writer(path) as w:
            w.write(str.encode(json.dumps(data, indent=4)))


def read_folder_input(path, folder_name="base_data", data_type="DF"):
    folder = get_folder(folder_name)
    if data_type == "DF":
        with folder.get_download_stream(path) as reader:
            data = pd.read_csv(reader)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")  # Ignore all warnings within this block
                data = function_with_warning(data)
    elif data_type == "JSON":
        with folder.get_download_stream(path) as reader:
            data = json.loads(reader.data)
    return data


def function_with_warning(df):
    for c in df.columns:
        if df[c].dtype == "object":
            temp_col = pd.to_datetime(df[c],  errors='coerce')
            if temp_col.notna().all():
                df[c] = temp_col
    return df
        
