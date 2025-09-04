import pandas as pd


def main(project_handle, client_d = {}):
    df = pd.json_normalize(project_handle.list_agent_tools())
df = rename_and_move_first(project_handle, df, "projectKey", "project_key")