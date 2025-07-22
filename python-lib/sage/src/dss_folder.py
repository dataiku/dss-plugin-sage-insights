# plugin: src.dss_folder
import dataiku
import pandas as pd
import json
import warnings


# ---------- DATAIKU LOCAL FOLDERS -----------------------------
def get_folder(sage_project_key, project_handle, folder_name):
    folder = dataiku.Folder(
        lookup = folder_name,
        project_key = sage_project_key,
        ignore_flow = True
        )
    try:
        folder.get_id()
    except:
        folder = create_folder(project_handle, folder_name)
    return folder


def create_folder(project_handle, folder_name):
    folder_handle = project_handle.create_managed_folder(
        name = folder_name,
        connection_name = "filesystem_folders"
    )
    if folder_name == "partitioned_data":
        settings = folder_handle.get_settings()
        settings.remove_partitioning()
        settings.add_discrete_partitioning_dimension("instance_name")
        settings.add_discrete_partitioning_dimension("category")
        settings.add_discrete_partitioning_dimension("module")
        settings.add_time_partitioning_dimension("date", period='DAY')
        settings.set_partitioning_file_pattern("%{instance_name}/%{category}/%{module}/%Y/%M/%D/.*")
        settings.save()
    return


def write_local_folder_output(sage_project_key, project_handle, folder_name, path, data, data_type="DF"):
    folder = get_folder(sage_project_key, project_handle, folder_name)
    if data_type == "DF":
        with folder.get_writer(path) as w:
            w.write(data.to_csv(index=False).encode("utf-8"))
    elif data_type == "JSON":
        with folder.get_writer(path) as w:
            w.write(str.encode(json.dumps(data, indent=4)))
    return


def read_local_folder_input(sage_project_key, project_handle, folder_name, path, data_type="DF"):
    folder = get_folder(sage_project_key, project_handle, folder_name)
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


# ---------- DATAIKU REMOTE FOLDERS ----------------------------
def write_remote_folder_output(self, client, path, df):
    projet_handle = client.get_project(project_key=self.sage_project_key)
    fid = None
    for f in projet_handle.list_managed_folders():
        if f["name"] == "partitioned_data":
            fid = f["id"]
            break
    if not fid:
        raise Exception()
    folder = projet_handle.get_managed_folder(odb_id=fid)
    r = folder.put_file(path, df.to_csv(index=None))
    return