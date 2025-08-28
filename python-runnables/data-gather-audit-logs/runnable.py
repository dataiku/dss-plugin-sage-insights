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
        df = pd.concat(dfs, ignore_index=True)
        results.append(["Gather Audit Logs", True, None])
        
        # get the cache timestamp and latest logs
        project_handle = local_client.get_default_project()
        dataset_handle = project_handle.get_dataset(dataset_name="audit_log_cache")
        if not dataset_handle.exists():
            builder = project_handle.new_managed_dataset("audit_log_cache")
            builder.with_store_into("filesystem_managed")
            dataset_handle = builder.create()
        dataset = dataiku.Dataset("audit_log_cache")
        try:
            audit_log_cache_df = dataset.get_dataframe()
        except:
            audit_log_cache_df = pd.DataFrame([datetime.now().astimezone()], columns=["timestamp"])
        last_update = audit_log_cache_df["timestamp"].iloc[0]        
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        #df = df[df["timestamp"] >= last_update]
        results.append(["Parse Latest Logs", True, None])
        
        # Expand Messages and join
        jdf = pd.json_normalize(df["message"]).add_prefix("message.").reset_index(drop=True)
        df = df.drop(columns="message").reset_index(drop=True)
        df = pd.concat([df, jdf], axis=1)
        
        # Column Cleanse
        df["timestamp"] = pd.to_datetime(audit_df["timestamp"])
        df["date"] = df["timestamp"].dt.date
        df["instance_name"] = instance_name

        # Module Import
        ## TODO: Scrape data, append to the current day log file, if it runs over midnight, figure out how to split logs
        ## r = user_login(self, remote_client, df)
        ###results.append(["User Audit", r[0], r[1]])

        ## event_mapping(df, self)
        ###results.append(["Event Mapping", result[0], result[1]])        
        ## cru_logs(df)
        ###results.append(["CRU Logs", result[0], result[1]])
        
        # Reset the audit_log_cache df
        last_time_entry = df["timestamp"].max()
        audit_log_cache_df["timestamp"] = last_time_entry
        dataset.write_with_schema(audit_log_cache_df)
        results.append(["Set New Audit Log Cache timestamp", True, last_time_entry])
        
        # return results
        results_df = pd.DataFrame(results, columns=["step", "result", "message"])
        html = results_df.to_html()
        return html


# EOF