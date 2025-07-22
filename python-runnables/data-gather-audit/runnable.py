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
        self.dt = datetime.utcnow()
        
    def get_progress_target(self):
        return None

    def run(self, progress_callback):
        # Get local client and name
        local_client = dss_funcs.build_local_client()
        instance_name = dss_funcs.get_dss_name(local_client)
        
        # change directory and get audit logs
        root_path = local_client.get_instance_info().raw["dataDirPath"]
        audit_path = f"{root_path}/run/audit"
        os.chdir(audit_path)
        directory_path = "./"
        logs = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

        # Open and read each log
        results = []
        today = date.today()
        yesterday = today - timedelta(days=1)
        df = pd.DataFrame()
        for log in logs:
            tdf = pd.read_json(log, lines=True)
            if df.empty:
                df = tdf
            else:
                df = pd.concat([df, tdf], ignore_index=True)
            df = df[
                (df["timestamp"].dt.date < today)
                & (df["timestamp"].dt.date >= yesterday)
            ]
        results.append(["read/parse", True, None])
        
        # loop topics and save data
        remote_client = dss_funcs.build_remote_client(self.sage_project_url, self.sage_project_api)
        dt_year  = str(self.dt.year)
        dt_month = str(f'{self.dt.month:02d}')
        dt_day   = str(f'{self.dt.day:02d}')
        for topic in df.topic.unique():
            try:
                write_path = f"/{instance_name}/audit/{topic}/{dt_year}/{dt_month}/{dt_day}/data.csv"
                dss_folder.write_remote_folder_output(self, remote_client, write_path, df)
                results.append(["write/save", True, None])
            except Exception as e:
                results.append(["write/save", False, e])
            
        # return results
        if results:
            df = pd.DataFrame(results, columns=["step", "result", "message"])
            html = df.to_html()
            return html
        raise Exception("FAILED TO RUN INSTANCE CHECKS")