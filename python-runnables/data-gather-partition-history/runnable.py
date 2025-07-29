import dataiku
import pandas as pd

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
        
        # build partition table
        folder = dataiku.Folder(
            lookup="partitioned_data",
            project_key=self.sage_project_key
        )
        df = pd.DataFrame(folder.list_partitions(), columns=["partition"])
        df[["instance_name", "category", "module", "dt"]] = df["partition"].str.split("|", expand=True)
        results.append(["Gather Partitions", True, None])
        
        # Audit log User information
        try:
            audit_user.main(df)
            results.append(["User Aduit", True, None])
        except Exception as e:
            results.append(["User Aduit", False, e])
        
        # return results
        if results:
            df = pd.DataFrame(results, columns=["step", "result", "message"])
            html = df.to_html()
            return html
        raise Exception("FAILED TO RUN PROJECT CHECKS")