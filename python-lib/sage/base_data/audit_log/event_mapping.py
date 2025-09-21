import pandas as pd
from io import StringIO
from sage.src import dss_folder, dss_funcs
from sage.base_data.audit_log import mapping


def parse_auth_llm(auth_list):
    project_key, webapp_id, user = None, None, None

    for item in auth_list:
        if isinstance(item, str) and "ticket:Standard webapp backend:" in item:
            part = item.split(":")[-1].strip()
            if "." in part:
                project_key, webapp_id = part.split(".", 1)
        elif isinstance(item, str):
            user = item

    return pd.Series([project_key, webapp_id, user],
                     index=["llm_webapp_project_key", "llm_webapp_id", "llm_webapp_user"])



def main(self, remote_client, df):
    results = []
    instance_name = df["instance_name"].iloc[0]
    mapping_df = pd.read_csv(StringIO(mapping.raw_csv))
    
    df = df[df["topic"] == "generic"].reset_index(drop=True)

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
        merged_df.columns = merged_df.columns.str.lower()
        merged_df.columns = merged_df.columns.str.replace('message_', '', regex=False)
        merged_df["dataiku_category"] = merged_df["dataiku_category"].str.lower()
        
        # AuthVia
        merged_df["authvia"] = merged_df["authvia"].where(~merged_df["authvia"].isna(), other=[ ])
        merged_df["authvia"] = merged_df["authvia"].apply(lambda x: ', '.join(map(str, x)))
        merged_df[["message_project_key_temp", "message_webapp_id"]] = merged_df["authvia"].apply(parse_authvia)
        if "project_key" not in merged_df.columns:
            merged_df["project_key"] = None
        merged_df["project_key"] = merged_df["project_key"].fillna(merged_df["message_project_key_temp"])   
                
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
