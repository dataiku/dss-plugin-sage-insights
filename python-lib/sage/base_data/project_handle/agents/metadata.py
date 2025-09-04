import pandas as pd
from sage.src import dss_funcs


def main(project_handle, client_d = {}):
    prefix = "agents"
    df = pd.json_normalize(project_handle.list_agents()).add_prefix(f"{prefix}_")
    df = df.explode(f"{prefix}_versions").reset_index(drop=True)
    df = pd.concat([
        df.drop(columns=[f"{prefix}_versions"]),
        pd.json_normalize(df[f"{prefix}_versions"]).add_prefix(f"{prefix}_verions_")
    ], axis=1)
    df.columns = df.columns.str.replace('.', '_', regex=False)
    df = rename_and_move_first(project_handle, df, "projectKey", "project_key")
    return df