import pandas as pd
from sage.src.dss_funcs import get_nested_value


def main(project_handle, client_d = {}):
    if not project_handle.list_datasets():
        return pd.DataFrame()
    
    dfs = []
    for dataset in project_handle.list_datasets():
        d = {"project_key": project_handle.project_key}
        
        # Poll Data
        d["dataset_name"] = dataset.get("name", False)
        d["dataset_type"] = dataset.get("type", False)
        d["dataset_managed"] = dataset.get("managed", False)
        d["dataset_formatType"] = get_nested_value(dataset, ["formatType"])
        d["dataset_last_mod_by"] = get_nested_value(dataset, ["versionTag", "lastModifiedBy", "login"])
        d["dataset_last_mod_dt"] = get_nested_value(dataset, ["versionTag", "lastModifiedOn"])
        d["dataset_last_create_by"] = get_nested_value(dataset, ["creationTag", "lastModifiedBy", "login"])
        d["dataset_last_create_dt"] = get_nested_value(dataset, ["creationTag", "lastModifiedOn"])
        d["dataset_tags"] = dataset.get("tags", False)
        
        d["dataset_last_mod_dt"] = pd.to_datetime(d["dataset_last_mod_dt"], unit="ms")
        d["dataset_last_create_dt"] = pd.to_datetime(d["dataset_last_create_dt"], unit="ms")
        
        dfs.append(pd.DataFrame([d]))
    # turn to dataframe
    df = pd.concat(dfs, ignore_index=True)
    return df