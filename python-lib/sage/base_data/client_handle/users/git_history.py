import dataiku
import pandas as pd
import numpy as np
from joblib import Parallel, delayed
from datetime import datetime, date, timedelta


def split_work(client, project_keys):
    df = pd.DataFrame()
    for project_key in project_keys:
        project_handle = client.get_project(project_key=project_key)
        git_log = project_handle.get_project_git().log()
        tdf = pd.DataFrame(git_log["entries"])
        if tdf.empty:
            continue
        tdf["timestamp"] = pd.to_datetime(tdf["timestamp"])
        tdf = tdf[
            (tdf["timestamp"].dt.date < today)
            & (tdf["timestamp"].dt.date >= yesterday)
        ]
        if df.empty:
            df = tdf
        else:
            df = pd.concat([df, tdf], ignore_index=True)
        df["project_key"] = project_key
    return df


def main(client):
    project_keys = client.list_project_keys()
    pkey_array = np.array_split(project_keys, 4)
    today = date.today()
    yesterday = today - timedelta(days=1)
    results = Parallel(n_jobs=4)(delayed(split_work)(client=client, project_keys=i) for i in pkey_array)
    df = pd.concat(results, ignore_index=True)
    return df