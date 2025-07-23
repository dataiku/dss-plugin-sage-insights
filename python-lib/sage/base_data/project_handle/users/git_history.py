import pandas as pd
from sage.src.dss_funcs import get_nested_value


def main(project_handle):
    d = {}
    
    project_handle = local_client.get_project(project_key=project_key)
    try:
        git_log = project_handle.get_project_git().log()
    except:
        continue
    for entry in git_log["entries"]:
        if "recipe" in entry["message"] and "recipe:" in entry["message"]:
            author = entry["author"]
            message = entry["message"]
            full_recipe_name = message.split(" ")[-1]
            project_name, recipe_name = full_recipe_name.split(".")
            recipe_handle = project_handle.get_recipe(recipe_name)
            try:
                recipe_type = recipe_handle.get_settings().data["recipe"]["type"]
                if not d.get(author, False):
                    d[author] = {}
                if d[author].get(recipe_type, False):
                    d[author][recipe_type] += 1
                else:
                    d[author][recipe_type] = 1
            except:
                continue