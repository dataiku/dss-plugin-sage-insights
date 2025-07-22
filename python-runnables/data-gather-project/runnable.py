try:
    from sage.base_data import project_handle as dss_objs
except:
    dss_objs = False
from sage.src import dss_funcs

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
        self.dt = datetime.utcnow()
        
    def get_progress_target(self):
        return None

    def run(self, progress_callback):
        # Test if modules are found
        if not dss_objs:
            raise Exception("No categories or modules found")
        
        # Collect the modules && Run the modules
        local_client = dss_funcs.build_local_client()
        results = []
        for key in local_client.list_project_keys():
            project_handle = local_client.get_project(project_key=key)
            results += dss_funcs.run_modules(self, dss_objs, project_handle, key)
        
        # return results
        if results:
            df = pd.DataFrame(results, columns=["project_key", "path", "module_name", "step", "result", "message"])
            html = df.to_html()
            return html
        raise Exception("FAILED TO RUN PROJECT CHECKS")