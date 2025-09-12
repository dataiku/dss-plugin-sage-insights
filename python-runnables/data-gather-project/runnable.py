try:
    from sage.base_data import project_handle as dss_objs
except:
    dss_objs = False
from sage.src import dss_funcs

import os
import pandas as pd
from datetime import datetime

from dataiku.runnables import Runnable


class MyRunnable(Runnable):
    def __init__(self, project_key, config, plugin_config):
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        self.sage_project_key = plugin_config.get("sage_project_key", None)
        self.sage_project_url = plugin_config.get("sage_project_url", None)
        self.sage_project_api = plugin_config.get("sage_project_api", None)
        self.ignore_certs     = plugin_config.get("ignore_certs", False)
        self.dt = datetime.utcnow()
        
        # Set environment variable
        self.sage_folder_connection = plugin_config.get("sage_folder_connection", "filesystem_folders")
        os.environ["SAGE_FOLDER_CONNECTION"] = self.sage_folder_connection
        
    def get_progress_target(self):
        return None

    def run(self, progress_callback):
        # Test if modules are found
        if not dss_objs:
            raise Exception("No categories or modules found")

        # Build Local Client
        local_client = dss_funcs.build_local_client()
        
        # Grab some exra details
        client_d = {}
        try:
            client_d["python_env_name"] = client.get_general_settings().settings["codeEnvs"]["defaultPythonEnv"]
            if not client_d["python_env_name"]:
                client_d["python_env_name"] = "USE_BUILTIN_MODE"
        except:
            client_d["python_env_name"] = "USE_BUILTIN_MODE"
        try:
            client_d["r_env_name"] = client.get_general_settings().settings["codeEnvs"]["defaultREnv"]
            if not client_d["r_env_name"]:
                client_d["r_env_name"] = "USE_BUILTIN_MODE"
        except:
            client_d["r_env_name"] = "USE_BUILTIN_MODE"
        try:
            client["container_env_name"] = client.get_general_settings().settings["containerSettings"]["defaultExecutionConfig"]
            if not client_d["container_env_name"]:
                client_d["container_env_name"] = "DSS_LOCAL"
        except:
            client_d["container_env_name"] = "DSS_LOCAL"
        
        # Collect the modules && Run the modules
        results = []
        for key in local_client.list_project_keys():
            project_handle = local_client.get_project(project_key=key)
            results += dss_funcs.run_modules(self, dss_objs, project_handle, client_d, key)
        
        # return results
        if results:
            # Save the df as a DS
            df = pd.DataFrame(results, columns=["project_key", "path", "module_name", "step", "result", "message"])
            df["timestamp"] = self.dt
            project_handle = local_client.get_default_project()
            dataset_handle = project_handle.get_dataset(dataset_name="dg_project_level")
            if not dataset_handle.exists():
                builder = project_handle.new_managed_dataset("dg_project_level")
                builder.with_store_into("filesystem_managed")
                dataset_handle = builder.create()
            dataset = dataiku.Dataset("audit_log_cache")
            dataset.write_with_schema(df)
            html = df.to_html()
            return html
        raise Exception("FAILED TO RUN PROJECT CHECKS")