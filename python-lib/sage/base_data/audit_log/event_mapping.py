import pandas as pd
from io import StringIO
from sage.src import dss_folder
from sage.base_data.audit_log import mapping


def main(self, remote_client, df):
    mapping_df = pd.read_csv(StringIO(mapping.raw_csv))
    
    # Select the columns needed
    try:
        df = df[["timestamp", "date", "message.msgType", "message.authUser", "message.projectKey", "instance_name"]]
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
        
        # Merge the mapping tables
        merged_df = pd.merge(
            grp,
            mapping_df,
            on="message.msgType",
            how="left"
        )
        
        # Filter - remove dropped columns
        merged_df = merged_df[merged_df["dataiku_category"] != "DROP_DELETE"]
        
        # lets split the df by category and save
        for category, sub_grp in merged_df.groupby("dataiku_category"):
            try:
                write_path = f"/{instance_name}/dataiku_usage/{category}/{dt_year}/{dt_month}/{dt_day}/data-{dt_epoch}.csv"
                dss_folder.write_remote_folder_output(self, remote_client, write_path, login_users_df)
                results.append([f"write/save - Dataiku Usage {category}", True, f"data-{dt_epoch}.csv"])
            except Exception as e:
                results.append(["write/save - All", False, e])
            
    return results
