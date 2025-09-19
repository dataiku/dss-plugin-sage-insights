import pandas as pd
from sage.src import dss_folder


def main(self, remote_client, df):
    return ["testing", True, "Testing"]
    # Remove scenarios, job and NaN's
    if "message_scenarioId" in df.columns:
        df = df[df["message_scenarioId"].isna()]
    if "message_jobId" in df.columns:
        df = df[df["message_jobId"].isna()]
    df = df[df["message_authSource"] == "USER_FROM_UI"]
    df = df.dropna(subset=["message_login"])
    df = df.dropna(axis=1, how='all')
    

    # Select the columns needed
    try:
        df = df[["timestamp", "date", "message_callPath", "message_msgType", "message_login", "message_project_key", "instance_name"]]
    except:
        return ["Loading Audit Logs", False, "No new data found"]

    results = []
    instance_name = df["instance_name"].iloc[0]
    # Loop over any partitions of dates for data
    for i,grp in df.groupby("date"):
        # datetime for saving
        dt = grp["timestamp"].max()
        dt_year  = str(dt.year)
        dt_month = str(f'{dt.month:02d}')
        dt_day   = str(f'{dt.day:02d}')
        dt_epoch = dt.value
        
        continue

        # Login Users
        login_users = grp[grp["message_msgType"] == "application-open"]["message_login"].unique()
        login_users_df = pd.DataFrame(login_users, columns=["viewing_user_logins"])
        login_users_df["timestamp"] = pd.to_datetime(i)
        login_users_df["instance_name"] = instance_name
        try:
            login_users_df.columns = login_users_df.columns.str.replace('message_', '', regex=False)
            write_path = f"/{instance_name}/users/viewing_user_logins/{dt_year}/{dt_month}/{dt_day}/data-{dt_epoch}.parquet"
            dss_folder.write_remote_folder_output(self, remote_client, write_path, login_users_df)
            results.append(["write/save", True, f"login users data-{dt_epoch}.parquet"])
        except Exception as e:
            results.append(["write/save - All", False, e])
        
        # Developer Users
        tdf = grp[grp["message_login"].isin(login_users)]
        ## Action Items
        action_words = ["save", "create", "analysis", "clear", "run"] # Action Words -- Focus on
        pattern = "|".join(action_words)
        tdf = tdf[tdf["message_msgType"].str.contains(pattern, na=False)]
        ## Bad items
        remove_strings = ["list", "dataset-clear-samples", "dataset-save-schema", "project-save-variables"] # Vague Words -- Remove
        pattern = "|".join(remove_strings)
        tdf = tdf[~tdf["message_msgType"].str.contains(pattern, na=False)]
        ## Unique it
        developer_users = tdf["message_login"].unique()
        developer_users_df = pd.DataFrame(developer_users, columns=["developer_user_logins"])
        developer_users_df["timestamp"] = pd.to_datetime(i)
        try:
            developer_users_df.columns = developer_users_df.columns.str.replace('message_', '', regex=False)
            write_path = f"/{instance_name}/users/developer_user_logins/{dt_year}/{dt_month}/{dt_day}/data-{dt_epoch}.parquet"
            dss_folder.write_remote_folder_output(self, remote_client, write_path, developer_users_df)
            results.append(["write/save", True, f"developing users data-{dt_epoch}.parquet"])
        except Exception as e:
            results.append(["write/save - All", False, e])
    
    return results