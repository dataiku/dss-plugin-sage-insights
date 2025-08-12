import pandas as pd
from sage.src.dss_funcs import get_nested_value


def main(project_handle):
    df = pd.DataFrame()
    for recipe in project_handle.list_recipes():
        d = {"project_key": project_handle.project_key}
        
        # Poll Data
        d["recipe_name"] = recipe["name"]
        d["recipe_type"] = recipe["type"]
        d["recipe_last_mod_by"] = get_nested_value(recipe, ["versionTag", "lastModifiedBy", "login"])
        d["recipe_last_mod_dt"] = get_nested_value(recipe, ["versionTag", "lastModifiedOn"])
        d["recipe_last_create_by"] = get_nested_value(recipe, ["creationTag", "lastModifiedBy", "login"])
        d["recipe_last_create_dt"] = get_nested_value(recipe, ["creationTag", "lastModifiedOn"])
        d["recipe_tags"] = recipe["tags"]
        
        d["recipe_last_mod_dt"] = pd.to_datetime(d["recipe_last_mod_dt"], unit="ms")
        d["recipe_last_create_dt"] = pd.to_datetime(d["recipe_last_create_dt"], unit="ms")
        
        # turn to dataframe
        tdf = pd.DataFrame([d])
        if df.empty:
            df = tdf
        else:
            df = pd.concat([df, tdf], ignore_index=True)
    return df