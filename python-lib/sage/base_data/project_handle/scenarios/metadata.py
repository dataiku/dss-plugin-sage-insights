import pandas as pd
from sage.src import dss_funcs


def main(self, project_handle, client_d = {}):
    if not project_handle.list_scenarios():
        return pd.DataFrame()
    
    prefix = "scenarios_"
    df = pd.json_normalize(project_handle.list_scenarios()).add_prefix(prefix)
    # Clean dates
    for c in ["scenarios_nextRun", "scenarios_lastModifiedOn", "scenarios_createdOn"]:
        df[c] = pd.to_datetime(df[c], unit="ms", utc=True)
        df[c] = df[c].fillna(pd.to_datetime("1970-01-01", utc=True))
        df[c] = df[c].dt.strftime("%Y-%m-%d %H:%M:%S.%f")
    # Project Key
    df = rename_and_move_first(project_handle, df, f"{prefix}projectKey", "project_key")
    return df