# sage/src/dss_folder.py
## Last Modified: 2025-09-12
# -----------------------------------------------------------------------------------------
import dataiku
import pandas as pd
import io


# ---------- DATAIKU LOCAL FOLDERS --------------------------------------------------------
def create_local_folder(self, project_handle, folder_name):
    folder_handle = project_handle.create_managed_folder(
        name = folder_name,
        connection_name = self.SAGE_FOLDER_CONNECTION
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


def get_local_folder(self, project_handle, folder_name):
    folder = dataiku.Folder(
        lookup = folder_name,
        project_key = self.sage_project_key,
        ignore_flow = True
    )
    try:
        folder.get_id()
    except:
        try:
            folder = create_local_folder(self, project_handle, folder_name)
        except Exception as e:
            raise Exception(e)
    return folder


def function_with_warning(df):
    for c in df.columns:
        if df[c].dtype == "object":
            temp_col = pd.to_datetime(df[c],  errors='coerce')
            if temp_col.notna().all():
                df[c] = temp_col
                min_date = df[df[c] != "1970-01-01"][c].min()
                df.loc[df[c] == "1970-01-01", c] = min_date
    return df


def read_local_folder_input(self, project_handle, folder_name, path):
    folder = get_folder(self, project_handle, folder_name)
    with folder.get_download_stream(path) as stream:
        file_bytes = io.BytesIO(stream.read())
        data = pd.read_parquet(file_bytes)
    return data


def write_local_folder_output(self, project_handle, folder_name, path, data):
    folder = get_folder(self, project_handle, folder_name)
    f = io.BytesIO()
    data.to_parquet(f)
    f.seek(0)
    content = f.read()
    folder.upload_stream(path, content)
    return


# ---------- DATAIKU REMOTE FOLDERS --------------------------------------------------------
def write_remote_folder_output(self, client, path, df):
    project_handle = client.get_project(project_key=self.sage_project_key)
    fid = None
    for f in project_handle.list_managed_folders():
        if f["name"] == "partitioned_data":
            fid = f["id"]
            break
    if not fid:
        raise Exception()
    folder = project_handle.get_managed_folder(odb_id=fid)
    r = folder.put_file(path, df.to_parquet(index=None))
    return