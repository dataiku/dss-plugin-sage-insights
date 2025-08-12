from sage.src import dss_funcs, dss_folder

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
        self.dt = datetime.utcnow()
        
    def get_progress_target(self):
        return None

    def run(self, progress_callback):
        results = []
        # get partitioned folder
        local_client = dss_funcs.build_local_client()
        project_handle = local_client.get_project(project_key=self.sage_project_key)
        folder = dss_folder.get_folder(self.sage_project_key, project_handle, "partitioned_data")
        
        # list partitions and turn into a df
        partitions = folder.list_partitions()
        folder_df = pd.DataFrame(partitions, columns=["partitions"])
        cols = ["instance_name", "category", "module", "dt"]
        folder_df[cols] = folder_df["partitions"].str.split("|", expand=True)
        results.append(["List Partitions", True, None])
        
        # get latest partition
        max_date = folder_df['dt'].max()
        dss_folder.write_local_folder_output(
            sage_project_key = self.sage_project_key,
            project_handle = project_handle,
            folder_name = "base_data",
            path = f"/partition.csv",
            data_type = "DF",
            data = pd.DataFrame([max_date], columns=["latest_partition"])
        )
        filtered_df = folder_df[folder_df['dt'] == max_date]
        results.append(["Newest Partition", True, None])
        
        # Loop over the sets and gather
        groups = filtered_df.groupby(by=["category", "module"])
        for i, g in groups:
            category, module = i
            # loop over and build consolidated df
            df = pd.DataFrame()
            for partition in g["partitions"].tolist():
                paths = folder.list_paths_in_partition(partition=partition)
                for path in paths:
                    tdf = dss_folder.read_local_folder_input(
                        sage_project_key = self.sage_project_key,
                        project_handle = project_handle,
                        folder_name = "partitioned_data",
                        path = path
                    )
                    if df.empty:
                        df = tdf
                    else:
                        df = pd.concat([df, tdf], ignore_index=True)
                # Write consolidated DF to folder
                dss_folder.write_local_folder_output(
                    sage_project_key = self.sage_project_key,
                    project_handle = project_handle,
                    folder_name = "base_data",
                    path = f"/{category}/{module}.csv",
                    data_type = "DF",
                    data = df
                )
        results.append(["Stack newest datasets", True, None])
        
        
        # Collapse all the metadata files down to 1 single dataset - One dataset to rule them all
        df = dss_folder.read_local_folder_input(
            sage_project_key = self.sage_project_key,
            project_handle = project_handle,
            folder_name = "base_data",
            path = "/users/metadata.csv"
        )
        for category in ["projects", "datasets", "recipes", "scenarios"]:
            category_df = dss_folder.read_local_folder_input(
                sage_project_key = self.sage_project_key,
                project_handle = project_handle,
                folder_name = "base_data",
                path = f"/{category}/metadata.csv"
            )
            if category == "projects":
                df = pd.merge(df, category_df, how="left", left_on=["instance_name", "login"], right_on=["instance_name", "login"])
            elif category == "datasets":
                df = pd.merge(df, category_df, how="left", on=["instance_name", "project_key"])
            elif category == "recipes":
                df = pd.merge(df, category_df, how="left", on=["instance_name", "project_key"])
            elif category == "scenarios":
                df = pd.merge(df, category_df, how="left", on=["instance_name", "project_key"])
                
        primary_keys = ["instance_name", "project_key", "enabled", "userProfile", "login"]
        df = df[primary_keys]
        dss_folder.write_local_folder_output(
            sage_project_key = self.sage_project_key,
            project_handle = project_handle,
            folder_name = "base_data",
            path = "/metadata_primary_keys.csv",
            data_type = "DF",
            data = df
        )
        results.append(["Metadata Master", True, None])
        
        # return results
        if results:
            df = pd.DataFrame(results, columns=["step", "result", "message"])
            html = df.to_html()
            return html
        raise Exception("FAILED TO RUN PROJECT CHECKS")