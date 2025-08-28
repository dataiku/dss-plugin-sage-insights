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
    return
