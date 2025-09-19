import pandas as pd
from io import StringIO
from sage.src import dss_folder, dss_funcs
from sage.base_data.audit_log import mapping


def main(self, remote_client, df):
    results = []
    instance_name = df["instance_name"].iloc[0]
    mapping_df = pd.read_csv(StringIO(mapping.raw_csv))

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
            on="message_msgType",
            how="left"
        )
        
        # Filter - remove dropped columns
        merged_df = merged_df[merged_df["dataiku_category"] != "DROP_DELETE"]
        merged_df["dataiku_category"] = merged_df["dataiku_category"].str.lower()
        merged_df.columns = merged_df.columns.str.replace('message_', '', regex=False)
                
        # lets split the df by category and save
        for category, grp in merged_df.groupby("dataiku_category"):
            grp = grp.dropna(axis=1, how='all').reset_index(drop=True)
            try:
                write_path = f"/{instance_name}/dataiku_usage/{category}/{dt_year}/{dt_month}/{dt_day}/data-{dt_epoch}.parquet"
                dss_folder.write_remote_folder_output(self, remote_client, write_path, grp)
                results.append([f"write/save - Dataiku Usage {category}", True, f"data-{dt_epoch}.parquet"])
            except Exception as e:
                results.append([f"write/save - Dataiku Usage {category}", False, e])
            
    return results
