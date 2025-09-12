import sys
sys.dont_write_bytecode = True

import dataiku
import pandas as pd
import json
import warnings
import os


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


def create_folder(self, project_handle, folder_name):
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


# ---------- DATAIKU REMOTE FOLDERS ----------------------------
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
    r = folder.put_file(path, df.to_csv(index=None))
    return