import pandas as pd
from sage.src import dss_funcs


def main(self, client, client_d = {}):
    project_handle = client.get_project(self.sage_worker_key)
    if not project_handle.list_llms():
        return pd.DataFrame()
    
    prefix = "llms"
    df = pd.json_normalize(project_handle.list_llms()).add_prefix(f"{prefix}_")
    df.drop(columns=["project_key"], inplace=True)
    return df