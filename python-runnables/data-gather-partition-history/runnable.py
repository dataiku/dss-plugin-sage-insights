import dataiku
import os
import pandas as pd
from datetime import datetime

from sage.src import dss_funcs, dss_folder
from sage.partition_history import audit_user, git_history

from dataiku.runnables import Runnable

class MyRunnable(Runnable):
    def __init__(self, project_key, config, plugin_config):
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        self.sage_project_key = plugin_config.get("sage_project_key", None)
        self.sage_project_url = plugin_config.get("sage_project_url", None)
        self.sage_project_api = plugin_config.get("sage_project_api", None)
        self.dt = datetime.utcnow()
        
        # Set environment variable
        self.sage_folder_connection = plugin_config.get("sage_folder_connection", "filesystem_folders")
        os.environ["SAGE_FOLDER_CONNECTION"] = self.sage_folder_connection
        
    def get_progress_target(self):
        return None

    def run(self, progress_callback):
        results = []
        
        # get partitioned folder
        local_client = dss_funcs.build_local_client()
        project_handle = local_client.get_project(project_key=self.sage_project_key)
        folder = dss_folder.get_folder(self.sage_project_key, project_handle, "partitioned_data")
        df = pd.DataFrame(folder.list_partitions(), columns=["partition"])
        df[["instance_name", "category", "module", "dt"]] = df["partition"].str.split("|", expand=True)
        df["dt"] = pd.to_datetime(df["dt"])
        results.append(["Gather Partitions", True, None])
        
        # Audit log User information
        try:
            audit_user.main(self, project_handle, folder, df)
            results.append(["User Aduit", True, None])
        except Exception as e:
            results.append(["User Aduit", False, e])
            
        # Audit log User information
        try:
            git_history.main(self, project_handle, folder, df)
            results.append(["Git History", True, None])
        except Exception as e:
            results.append(["Git History", False, e])
        
        # return results
        if results:
            df = pd.DataFrame(results, columns=["step", "result", "message"])
            html = df.to_html()
            return html