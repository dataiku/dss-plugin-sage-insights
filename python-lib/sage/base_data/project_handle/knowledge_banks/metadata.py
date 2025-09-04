import pandas as pd
from sage.src import dss_funcs


def main(project_handle, client_d = {}):
    df = pd.json_normalize(project_handle.list_knowledge_banks()).add_prefix("agent_tools_")
    df = dss_funcs.rename_and_move_first(project_handle, df, "agent_tools_projectKey", "project_key")
    return df