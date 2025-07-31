import pandas as pd
from sage.src.dss_funcs import get_nested_value


def main(project_handle):
    df = pd.DataFrame()
    for recipe in project_handle.list_recipes():
        d = {"projectKey": project_handle.project_key}
        # Poll Data
        d["recipe_name"] = recipe["name"]
        d["recipe_type"] = recipe["type"]
        d["lastModifiedBy"] = get_nested_value(recipe, ["versionTag", "lastModifiedBy", "login"])
        d["lastModifiedOn"] = get_nested_value(recipe, ["versionTag", "lastModifiedOn"])
        d["creationBy"] = get_nested_value(recipe, ["creationTag", "lastModifiedBy", "login"])
        d["creationOn"] = get_nested_value(recipe, ["creationTag", "lastModifiedOn"])
        d["tags"] = recipe["tags"]
        # turn to dataframe
        tdf = pd.DataFrame([d])
        if df.empty:
            df = tdf
        else:
            df = pd.concat([df, tdf], ignore_index=True)
    return df