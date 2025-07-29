import dataiku
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
        self.dt = datetime.utcnow()
        
    def get_progress_target(self):
        return None

    def run(self, progress_callback):
        folder = dataiku.Folder(
            lookup="partitioned_data",
            project_key=self.sage_project_key
        )
        
        # build partition table
        df = pd.DataFrame(folder.list_partitions(), columns=["partition"])
        df[["instance_name", "category", "module", "dt"]] = df["partition"].str.split("|", expand=True)
        
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

        results.append(["Stack newest datasets", True, None])
                
        
        # return results
        if results:
            df = pd.DataFrame(results, columns=["step", "result", "message"])
            html = df.to_html()
            return html
        raise Exception("FAILED TO RUN PROJECT CHECKS")