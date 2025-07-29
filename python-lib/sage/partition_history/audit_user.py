from sage.src import dss_funcs, dss_folder

import pandas as pd

def main(self, project_handle, folder, df):
    # Select the partition
    partitions = df[
        (df["category"] == "users")
        & (df["module"] == "audit")
    ]["partition"].tolist()
    
    # Load the df
    login_users_df = pd.DataFrame()
    active_users_df = pd.DataFrame()
    for partition in partitions:
        for path in folder.get_partition_info(partition)["paths"]:
            with folder.get_download_stream(path=path) as r:
                df = pd.read_csv(r)
            
            # Login Users
            login_users = df[df["message.msgType"] == "application-open"]["message.authUser"].unique()
            login_users_tmp_df = pd.DataFrame([len(login_users)], columns=["count"])
            login_users_tmp_df["timestamp"] = df["timestamp"].iloc[0]
            login_users_tmp_df["instance_name"] = df["instance_name"].iloc[0]
            if login_users_df.empty:
                login_users_df = login_users_tmp_df
            else:
                login_users_df = pd.concat([login_users_df, login_users_tmp_df], ignore_index=True)

            # Active Users
            tdf = df[df["message.authUser"].isin(login_users)]
            action_words = ["save", "create", "analysis", "clear", "run"] # Action Words -- Focus on
            pattern = "|".join(action_words)
            tdf = tdf[tdf["message.msgType"].str.contains(pattern, na=False)]
            remove_strings = ["list", "dataset-clear-samples", "dataset-save-schema", "project-save-variables"] # Vague Words -- Remove
            pattern = "|".join(remove_strings)
            tdf = tdf[~tdf["message.msgType"].str.contains(pattern, na=False)]
            active_users = tdf["message.authUser"].unique()
            active_users_tmp_df = pd.DataFrame([len(active_users)], columns=["count"])
            active_users_tmp_df["timestamp"] = df["timestamp"].iloc[0]
            active_users_tmp_df["instance_name"] = df["instance_name"].iloc[0]
            if login_users_df.empty:
                active_users_df = active_users_tmp_df
            else:
                active_users_df = pd.concat([active_users_df, active_users_tmp_df], ignore_index=True)

    # Write consolidated DF to folder
    dss_folder.write_local_folder_output(
        sage_project_key = self.sage_project_key,
        project_handle = project_handle,
        folder_name = "base_data",
        path = f"/users/login_users.csv",
        data_type = "DF",
        data = login_users_df
    )
    dss_folder.write_local_folder_output(
        sage_project_key = self.sage_project_key,
        project_handle = project_handle,
        folder_name = "base_data",
        path = f"/users/active_users.csv",
        data_type = "DF",
        data = active_users_df
    )
    
    return