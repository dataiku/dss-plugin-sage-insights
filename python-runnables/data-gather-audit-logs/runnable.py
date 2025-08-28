from sage.src import dss_funcs, dss_folder

import os
import pandas as pd
from datetime import datetime, date, timedelta

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
        
    def get_progress_target(self):
        return None

    def run(self, progress_callback):
        raise Exception("unimplemented")
        