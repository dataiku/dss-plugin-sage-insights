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
        
        merged_df = pd.merge(
            grp,
            mapping_df,
            on="message.msgType",
            how="left"
        )

    return
