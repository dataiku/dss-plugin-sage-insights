import pandas as pd
from sage.src.dss_funcs import get_nested_value


def main(project_handle):
    df = pd.DataFrame()
    for dataset in project_handle.list_datasets():
        d = {"projectKey": project_handle.project_key}
        
        # Poll Data
        ["dataset_name"] = dataset.get("name", False)
        ["dataset_type"] = dataset.get("type", False)
        ["dataset_managed"] = dataset.get("managed", False)
        ["dataset_formatType"] = get_nested_value(dataset, ["formatType"])
        ["dataset_last_mod_by"] = get_nested_value(dataset, ["versionTag", "lastModifiedBy", "login"])
        ["dataset_last_mod_dt"] = get_nested_value(dataset, ["versionTag", "lastModifiedOn"])
        ["dataset_last_create_by"] = get_nested_value(dataset, ["creationTag", "lastModifiedBy", "login"])
        ["dataset_last_create_dt"] = get_nested_value(dataset, ["creationTag", "lastModifiedOn"])
        ["tags"] = dataset.get("tags", False)
        
        # turn to dataframe
        tdf = pd.DataFrame([d])
        if df.empty:
            df = tdf
        else:
            df = pd.concat([df, tdf], ignore_index=True)
    return df