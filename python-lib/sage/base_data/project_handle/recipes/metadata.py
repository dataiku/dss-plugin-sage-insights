import pandas as pd
from sage.src.dss_funcs import get_nested_value


def main(project_handle, client_d = {}):
    # Get project level python code environment
    project_python_env = project_handle.get_settings().settings["settings"]["codeEnvs"]["python"]["mode"]
    if project_python_env == "USE_BUILTIN_MODE":
        python_env_name = "USE_BUILTIN_MODE"
    elif project_python_env == "INHERIT":
        python_env_name = client_d["python_env_name"]
    else:
        python_env_name = project_handle.get_settings().settings["settings"]["codeEnvs"]["python"]["envName"]
    
    project_r_env = project_handle.get_settings().settings["settings"]["codeEnvs"]["R"]["mode"]
    if project_r_env == "USE_BUILTIN_MODE":
        r_env_name = "USE_BUILTIN_MODE"
    elif project_r_env == "INHERIT":
        r_env_name = client_d["r_env_name"]
    else:
        r_env_name = project_handle.get_settings().settings["settings"]["codeEnvs"]["R"]["envName"]
        
    project_container_env = project_handle.get_settings().settings["settings"]["container"]["containerMode"]
    if project_container_env == "NONE":
        container_env_name = "DSS_LOCAL"
    elif project_container_env == "INHERIT":
        container_env_name = client_d["container_env_name"]
    else:
        container_env_name = project_handle.get_settings().settings["settings"]["container"]["containerConf"]
    
    # Loop Recipes
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
        
        # Get layer 2 information
        recipe_handle = project_handle.get_recipe(recipe["name"])
        if recipe["type"] == "python":
            d["recipe_code_env_mode"] = recipe_handle.get_settings().data["recipe"]["params"]["envSelection"]["envMode"]
            if d["recipe_code_env_mode"] == "USE_BUILTIN_MODE":
                d["recipe_code_env_name"] = "USE_BUILTIN_MODE"  
            elif d["recipe_code_env_mode"] == "INHERIT":
                d["recipe_code_env_name"] = python_env_name
            else:
                d["recipe_code_env_name"] = recipe_handle.get_settings().data["recipe"]["params"]["envSelection"]["envName"]
         
        if recipe["type"] == "R":
            d["recipe_code_env_mode"] = recipe_handle.get_settings().data["recipe"]["params"]["envSelection"]["envMode"]
            if d["recipe_code_env_mode"] == "USE_BUILTIN_MODE":
                d["recipe_code_env_name"] = "USE_BUILTIN_MODE"  
            elif d["recipe_code_env_mode"] == "INHERIT":
                d["recipe_code_env_name"] = r_env_name
            else:
                d["recipe_code_env_name"] = recipe_handle.get_settings().data["recipe"]["params"]["envSelection"]["envName"]
                
        if recipe["type"] in ["python", "R"]:
            d["recipe_container_mode"] = recipe_handle.get_settings().data["recipe"]["params"]["containerSelection"]["containerMode"]
            if d["recipe_container_mode"] == "NONE":
                d["recipe_container_name"] = "DSS_LOCAL"  
            elif d["recipe_container_mode"] == "INHERIT":
                d["recipe_container_name"] = container_env_name
            else:
                d["recipe_container_name"] = recipe_handle.get_settings().data["recipe"]["params"]["containerSelection"]["containerConf"]
        
        # turn to dataframe
        tdf = pd.DataFrame([d])
        if df.empty:
            df = tdf
        else:
            df = pd.concat([df, tdf], ignore_index=True)
    return df