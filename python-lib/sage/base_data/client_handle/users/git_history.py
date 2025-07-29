import dataiku
import pandas as pd
from datetime import datetime, date, timedelta


def main(client):
    project_keys = client.list_project_keys()
    d = {}
    for project_key in project_keys:
        project_handle = client.get_project(project_key=project_key)
        try:
            git_log = project_handle.get_project_git().log()
        except:
            return pd.DataFrame()
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
    
    # Create DF
    df = pd.DataFrame(d).T.reset_index(names="login")
    return df