import pandas as pd
from sage.src.dss_funcs import get_nested_value


def main(project_handle):
    cols = [
        "project_key", 
        "recipe_name",
        "recipe_type", 
        "lastModifiedBy",
        "lastModifiedOn",
        "creationBy",
        "creationOn",
        "tags"
    ]
    df = pd.DataFrame(columns=cols)
    for recipe in project_handle.list_recipes():
        projectKey = recipe["projectKey"]
        recipe_name = recipe["name"]
        recipe_type = recipe["type"]
        lastModifiedBy = get_nested_value(recipe, ["versionTag", "lastModifiedBy", "login"])
        lastModifiedOn = get_nested_value(recipe, ["versionTag", "lastModifiedOn"])
        creationBy = get_nested_value(recipe, ["creationTag", "lastModifiedBy", "login"])
        creationOn = get_nested_value(recipe, ["creationTag", "lastModifiedOn"])
        tags = recipe["tags"]
        d = [
            projectKey, recipe_name, recipe_type,
            lastModifiedBy, lastModifiedOn, creationBy, creationOn,
            tags
        ]
        tdf = pd.DataFrame([d], columns=cols)
        df = pd.concat([df, tdf], ignore_index=True)
    return df