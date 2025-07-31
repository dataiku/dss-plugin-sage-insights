import pandas as pd
from sage.src.dss_funcs import get_nested_value


def main(project_handle):
    df = pd.DataFrame()
    for dataset in project_handle.list_datasets():
        d = {"projectKey": project_handle.project_key}
        ["dataset_name"] = dataset.get("name", False)
        ["dataset_type"] = dataset.get("type", False)
        ["dataset_managed"] = dataset.get("managed", False)
        ["formatType"] = get_nested_value(dataset, ["formatType"])
        ["lastModifiedBy"] = get_nested_value(dataset, ["versionTag", "lastModifiedBy", "login"])
        ["lastModifiedOn"] = get_nested_value(dataset, ["versionTag", "lastModifiedOn"])
        ["creationBy"] = get_nested_value(dataset, ["creationTag", "lastModifiedBy", "login"])
        ["creationOn"] = get_nested_value(dataset, ["creationTag", "lastModifiedOn"])
        ["tags"] = dataset.get("tags", False)
        
        # turn to dataframe
        tdf = pd.DataFrame([d])
        if df.empty:
            df = tdf
        else:
            df = pd.concat([df, tdf], ignore_index=True)
    return df