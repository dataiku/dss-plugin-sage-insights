from sage.src import dss_funcs
from sage.src import dss_init

import pandas as pd

from dataiku.runnables import Runnable

class MyRunnable(Runnable):
    def __init__(self, project_key, config, plugin_config):
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        self.sage_project_key = plugin_config.get("sage_project_key", None)
        self.sage_project_url = plugin_config.get("sage_project_url", None)
        self.sage_project_api = plugin_config.get("sage_project_api", None)
        self.sage_worker_key  = plugin_config.get("sage_worker_key", None)
        self.repo = "https://github.com/mazzei-dataiku/sage.git"
        
    def get_progress_target(self):
        return None

    def run(self, progress_callback):
        results = []
        for api_config in self.plugin_config["api_configs"]:
            # Create a remote client
            worker_url = api_config["worker_url"]
            worker_api = api_config["worker_api"]
            remote_client = dss_funcs.build_remote_client(worker_url, worker_api)
            
            # Install Plugin if not found
            cont = True
            try:
                dss_init.install_plugin(self, remote_client)
                results.append([worker_url, "plugin_install", True, None])
            except Exception as e:
                results.append([worker_url, "plugin_install", False, e])
                cont = False
            
            # Create the Sage Worker Project
            if cont:
                try:
                    project_handle = dss_init.create_worker(remote_client, self.sage_worker_key)
                    results.append([worker_url, "project_handle", True, None])
                except Exception as e:
                    results.append([worker_url, "project_handle", False, e])
                    cont = False

            # Create the DSS Commit Table
            if cont:
                try:
                    dss_init.get_dss_commits(project_handle)
                    results.append([worker_url, "dss_commit", True, None])
                except Exception as e:
                    cont = False
                    results.append([worker_url, "dss_commit", False, e])
            
            # Create the Phone Home Scenarios
            if cont:
                try:
                    dss_init.create_scenarios(project_handle)
                    results.append([worker_url, "scenarios", True, None])
                except Exception as e:
                    cont = False
                    results.append([worker_url, "scenarios", False, e])
        
        # return results
        if results:
            df = pd.DataFrame(results, columns=["worker_url", "step", "results", "message"])
            html = df.to_html()
            return html      