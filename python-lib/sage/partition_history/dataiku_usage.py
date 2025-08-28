from sage.src import dss_folder

import pandas as pd

def main(self, project_handle, folder, df):
    for module in df["module"][df["category"] == "dataiku_usage"].unique().tolist():
        # Get a partitions df for the module
        partitions_df = df[
            (df["category"] == "dataiku_usage")
            & (df["module"] == module)
        ]
        # try to pull last update time to keep only the newest partitions
        try:
            original_df = dss_folder.read_local_folder_input(
                sage_project_key = self.sage_project_key,
                project_handle = project_handle,
                folder_name = "base_data", 
                path = f"/dataiku_usage/rolling_{module}.csv"
            )
            last_entry = original_df["timestamp"].max()
        except:
            original_df = pd.DataFrame()
            last_entry = pd.to_datetime(1970)
        # Read in the new partitions and update the csv
        partitions_df = partitions_df.loc[partitions_df["dt"] >= last_entry]
        partitions = partitions_df["partition"].tolist()
        if not partitions:
            continue
        for partition in partitions:
            dfs = []
            for path in folder.get_partition_info(partition)["paths"]:
                with folder.get_download_stream(path=path) as r:
                    dfs.append(pd.read_csv(r))
            tdf = pd.concat(dfs, ignore_index=True)
            original_df = pd.concat([original_df, tdf], ignore_index=True)
        # Write new output
        original_df = original_df.drop_duplicates()
        original_df = original_df.sort_values(by="timestamp", ascending=False)
        dss_folder.write_local_folder_output(
            sage_project_key = self.sage_project_key,
            project_handle = project_handle,
            folder_name = "base_data",
            path = f"/dataiku_usage/{module}.csv",
            data_type = "DF",
            data = original_df
        )
    return