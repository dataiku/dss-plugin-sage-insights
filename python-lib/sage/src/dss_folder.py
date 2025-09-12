import sys
sys.dont_write_bytecode = True

import dataiku
import pandas as pd
import json
import warnings
import os

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