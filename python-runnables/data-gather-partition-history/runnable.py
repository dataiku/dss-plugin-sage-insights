import dataiku
import os
import pandas as pd
from datetime import datetime

from sage.src import dss_funcs, dss_folder
from sage.partition_history import audit_user, git_history, dataiku_usage

from dataiku.runnables import Runnable, ResultTable

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
        # get partitioned folder
        local_client = dss_funcs.build_local_client()
        project_handle = local_client.get_project(project_key=self.sage_project_key)
        folder = dss_folder.get_local_folder(self, project_handle, "partitioned_data")
        
        # list partitions and turn into a df
        results = []
        partitions = folder.list_partitions()
        folder_df = pd.DataFrame(partitions, columns=["partitions"])
        cols = ["instance_name", "category", "module", "dt"]
        folder_df[cols] = folder_df["partitions"].str.split("|", expand=True)
        folder_df["dt"] = pd.to_datetime(folder_df["dt"])
        results.append(["List Partitions", True, None])
        
        # Audit log User information
        modules = {
            "User Audit": 'audit_user',
            "Dataiku Usage": 'dataiku_usage',
            "Git History": 'git_history',

        }
        for module in modules:
            try:
                modules[module].main(self, project_handle, folder, folder_df)
                results.append([module, True, None])
            except Exception as e:
                results.append([module, False, e])
            
        ## Git history
        #try:
        #    git_history.main(self, project_handle, folder, df)
        #    results.append(["Git History", True, None])
        #except Exception as e:
        #    results.append(["Git History", False, e])

        # return results
        if results:
            df = pd.DataFrame(results, columns=["step", "result", "message"])
            df = df.astype(str)
            rt = ResultTable()
            n = 1
            for col in df.columns:
                rt.add_column(n, col, "STRING")
                n +=1
            for index, row in df.iterrows():
                rt.add_record(row.tolist())
            return rt
        else:
            raise Exception("Something went wrong")
