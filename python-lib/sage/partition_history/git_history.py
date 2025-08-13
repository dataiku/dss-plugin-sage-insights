from sage.src import dss_funcs, dss_folder

import pandas as pd

def main(self, project_handle, folder, df):
    # Select the partition
    partitions = df[
        (df["category"] == "users")
        & (df["module"] == "git_history")
    ]["partition"].tolist()
    
    # Load the df
    git_history_df = pd.DataFrame()
    for partition in partitions:
        for path in folder.get_partition_info(partition)["paths"]:
            with folder.get_download_stream(path=path) as r:
                df = pd.read_csv(r)
            # Build Git History Table
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            git_history_tmp_df = df.groupby(["instance_name", "author", "project_key"])["author"].size().reset_index(name="count")
            git_history_tmp_df["timestamp"] = df["timestamp"].iloc[0].to_period("D")
            if git_history_df.empty:
                git_history_df = git_history_tmp_df
            else:
                git_history_df = pd.concat([git_history_df, git_history_tmp_df], ignore_index=True)

    # Simplify column name
    git_history_df = git_history_df.rename(columns={"author": "login"})

    # Write consolidated DF to folder
    dss_folder.write_local_folder_output(
        sage_project_key = self.sage_project_key,
        project_handle = project_handle,
        folder_name = "base_data",
        path = f"/users/rolling_git_history.csv",
        data_type = "DF",
        data = git_history_df
    )
    
    return