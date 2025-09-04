import pandas as pd
from sage.src import dss_funcs


def main(project_handle, client_d = {}):
    prefix = "agent_tools"
    df = pd.json_normalize(project_handle.list_agent_tools()).add_prefix(f"{prefix}_")
    df = dss_funcs.rename_and_move_first(project_handle, df, f"{prefix}_projectKey", "project_key")
    return df