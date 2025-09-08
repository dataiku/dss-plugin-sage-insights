import pandas as pd
import numpy as np
from joblib import Parallel, delayed
from sage.src.dss_funcs import get_nested_value


def project_gather(projects):
    dfs = []
    for project in projects:
        d = {}
        d["project_key"] = project.get("projectKey", False)
        d["project_name"] = project.get("name", False)
        d["login"] = project.get("ownerLogin", False) # Match users dataframe
        d["project_login_dn"] = get_nested_value(project, ["ownerDisplayName"])
        d["project_last_mod_by"] = get_nested_value(project, ["versionTag", "lastModifiedBy", "login"])
        d["project_last_mod_dt"] = get_nested_value(project, ["versionTag", "lastModifiedOn"])
        d["project_last_create_by"] = get_nested_value(project, ["creationTag", "lastModifiedBy", "login"])
        d["project_last_create_dt"] = get_nested_value(project, ["creationTag", "lastModifiedOn"])
        d["project_shortDesc"] = project.get("shortDesc", False)
        d["project_tags"] = project.get("tags", False)
        dfs.append(pd.DataFrame([d]))
    df = pd.concat(dfs, ignore_index=True)
    return df


def main(client, client_d = {}):
    dfs = []
    list_projects_arrays = np.array_split(client.list_projects(), 2)
    results = Parallel(n_jobs=2)(delayed(project_gather)(i) for i in list_projects_arrays)
    df = pd.concat(results, ignore_index=True)
    
    # Imported projects missing creation values - temp fix for now
    df.loc[df["project_last_create_by"] == False, "project_last_create_by"] = df["project_last_mod_by"]
    df.loc[df["project_last_create_dt"] == 0, "project_last_create_dt"]     = df["project_last_mod_dt"]

    # Clean dates
    for c in ["project_last_mod_dt", "project_last_create_dt"]:
        df[c] = pd.to_datetime(df[c], unit="ms", utc=True)
        df[c] = df[c].fillna(pd.to_datetime("1970-01-01", utc=True))
        df[c] = df[c].dt.strftime("%Y-%m-%d %H:%M:%S.%f")
    
    return df