import dataiku
import pandas as pd
from datetime import datetime

from sage.src import dss_funcs
from sage.partition_history import audit_user

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
        results.append(["Gather Partitions", True, None])
        
        # Audit log User information
        try:
            audit_user.main(self, project_handle, df)
            results.append(["User Aduit", True, None])
        except Exception as e:
            results.append(["User Aduit", False, e])
        
        # return results
        if results:
            df = pd.DataFrame(results, columns=["step", "result", "message"])
            html = df.to_html()
            return html
        raise Exception("FAILED TO RUN PROJECT CHECKS")