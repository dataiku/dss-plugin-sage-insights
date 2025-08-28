from sage.src import dss_funcs, dss_folder

import os
import time
from pathlib import Path
import pandas as pd
import dataiku
from datetime import datetime


from dataiku.runnables import Runnable


def find_recent_files(file_list, hours=6):
    recent_files = []
    cutoff = time.time() - (hours * 3600)  # seconds
    for file in file_list:
        path = Path(file)
        if path.exists():
            last_modified = path.stat().st_mtime
            if last_modified >= cutoff:
                recent_files.append(path)
    return recent_files


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
        results = []
        remote_client = dss_funcs.build_remote_client(
            self.sage_project_url, self.sage_project_api, self.ignore_certs
        )
        dt_year  = str(self.dt.year)
        dt_month = str(f'{self.dt.month:02d}')
        dt_day   = str(f'{self.dt.day:02d}')
        
        # Get local client and name
        local_client = dss_funcs.build_local_client()
        instance_name = dss_funcs.get_dss_name(local_client)
        
        # change directory and get audit logs
        root_path = local_client.get_instance_info().raw["dataDirPath"]
        audit_path = f"{root_path}/run/audit"
        os.chdir(audit_path)
        directory_path = "./"
        logs = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        logs = find_recent_files(logs)
        dfs = []
        for log in logs:
            df = pd.read_json(log, lines=True)
            dfs.append(df)
            
        # flatten the df
        df = pd.concat(dfs, ignore_index=True)
        jdf = pd.json_normalize(df["message"]).add_prefix("message.").reset_index(drop=True)
        df = df.drop(columns="message").reset_index(drop=True)
        df = pd.concat([df, jdf], axis=1)
        
        
        # return results
        if results:
            df = pd.DataFrame(results, columns=["step", "result", "message"])
            html = df.to_html()
            return html
        raise Exception("FAILED TO RUN INSTANCE CHECKS")
        
        