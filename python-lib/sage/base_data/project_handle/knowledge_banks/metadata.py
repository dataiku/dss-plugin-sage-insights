import pandas as pd
from sage.src import dss_funcs


def main(project_handle, client_d = {}):
    prefix = "knowledge_banks_"
    df = pd.json_normalize(project_handle.list_knowledge_banks()).add_prefix(prefix)
    df = dss_funcs.rename_and_move_first(project_handle, df, f"{prefix}projectKey", "project_key")
    return df