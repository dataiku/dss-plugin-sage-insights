import pandas as pd


def main(client, client_d = {}):
    connections = client.list_connections_names(connection_type="all")
    dfs = []
    for conn in connections:
        conn_handle = client.get_connection(name=conn)
        settings = conn_handle.get_settings()
        d = settings.settings
        dfs.append(pd.json_normalize(d))
    df = pd.concat(dfs, ignore_index=True)
    df.columns = df.columns.str.replace(".", "_", regex=False)
    return df