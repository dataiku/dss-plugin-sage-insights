import pandas as pd
from sage.src import dss_funcs


def main(project_handle, client_d = {}):
    prefix = "agents"
    df = pd.json_normalize(project_handle.list_agents())
    df = df.explode("versions").reset_index(drop=True)
    df = pd.concat([
        df.drop(columns=["versions"]),
        pd.json_normalize(df["versions"]).add_prefix("verions_")
    ], axis=1)
    df.columns = df.columns.str.replace('.', '_', regex=False)
    df = rename_and_move_first(project_handle, df, "projectKey", "project_key")
    return df