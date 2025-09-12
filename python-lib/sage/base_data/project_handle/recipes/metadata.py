import pandas as pd
from sage.src import dss_funcs


def main(self, project_handle, client_d = {}):
    if not project_handle.list_recipes():
        return pd.DataFrame()
    
    # Get project level python code environment
    project_python_env = project_handle.get_settings().settings["settings"]["codeEnvs"]["python"]["mode"]
    if project_python_env == "USE_BUILTIN_MODE":
        python_env_name = "USE_BUILTIN_MODE"
    elif project_python_env == "INHERIT":
        python_env_name = client_d["python_env_name"]
    else:
        python_env_name = project_handle.get_settings().settings["settings"]["codeEnvs"]["python"]["envName"]
    # Get project level python code environment
    project_r_env = project_handle.get_settings().settings["settings"]["codeEnvs"]["r"]["mode"]
    if project_r_env == "USE_BUILTIN_MODE":
        r_env_name = "USE_BUILTIN_MODE"
    elif project_r_env == "INHERIT":
        r_env_name = client_d["r_env_name"]
    else:
        r_env_name = project_handle.get_settings().settings["settings"]["codeEnvs"]["r"]["envName"]        
    # Get project level python code environment
    project_container_env = project_handle.get_settings().settings["settings"]["container"]["containerMode"]
    if project_container_env == "NONE":
        container_env_name = "DSS_LOCAL"
    elif project_container_env == "INHERIT":
        container_env_name = client_d["container_env_name"]
    else:
        container_env_name = project_handle.get_settings().settings["settings"]["container"]["containerConf"]
    # Build base df
    prefix = "recipes_"
    df = pd.json_normalize(project_handle.list_recipes()).add_prefix(prefix)
    # Clean dates
    for c in ["recipes_versionTag.lastModifiedOn", "recipes_creationTag.lastModifiedOn"]:
        df[c] = pd.to_datetime(df[c], unit="ms", utc=True)
        df[c] = df[c].fillna(pd.to_datetime("1970-01-01", utc=True))
        df[c] = df[c].dt.strftime("%Y-%m-%d %H:%M:%S.%f")
    # Project Key
    df = dss_funcs.rename_and_move_first(project_handle, df, f"{prefix}projectKey", "project_key")
    # Get layer 2 information
    for row in df.itertuples():
        recipes_name = getattr(row, "recipes_name")
        recipes_type = getattr(row, "recipes_type")
        recipe_engine_type = getattr(row, "recipe_engine_type")
        recipe_handle = project_handle.get_recipe(recipes_name)
        try:
            df["recipe_engine_type"] = recipe_handle.get_status().get_selected_engine_details()["type"]
            df["recipe_engine_label"] = recipe_handle.get_status().get_selected_engine_details()["label"]
            df["recipe_engine_recommended"] = recipe_handle.get_status().get_selected_engine_details()["recommended"]
        except:
            df["recipe_engine_type"] = "NOT_FOUND"
            df["recipe_engine_label"] = "NOT_FOUND"
            df["recipe_engine_recommended"] = "NOT_FOUND"
        if recipes_type == "python":
            recipe_code_env_mode = recipe_handle.get_settings().data["recipe"]["params"]["envSelection"]["envMode"]
            if recipe_code_env_mode == "USE_BUILTIN_MODE":
                df["recipe_code_env_name"] = "USE_BUILTIN_MODE"  
            elif recipe_code_env_mode == "INHERIT":
                df["recipe_code_env_name"] = python_env_name
            else:
                df["recipe_code_env_name"] = recipe_handle.get_settings().data["recipe"]["params"]["envSelection"]["envName"]
        # R
        if recipes_type == "R":
            recipe_code_env_mode = recipe_handle.get_settings().data["recipe"]["params"]["envSelection"]["envMode"]
            if recipe_code_env_mode == "USE_BUILTIN_MODE":
                df["recipe_code_env_name"] = "USE_BUILTIN_MODE"  
            elif recipe_code_env_mode == "INHERIT":
                df["recipe_code_env_name"] = r_env_name
            else:
                df["recipe_code_env_name"] = recipe_handle.get_settings().data["recipe"]["params"]["envSelection"]["envName"]
        # PYTHON / R
        if recipes_type in ["python", "R"]:
            recipe_container_mode = recipe_handle.get_settings().data["recipe"]["params"]["containerSelection"]["containerMode"]
            if recipe_container_mode == "NONE":
                df["recipe_container_name"] = "DSS_LOCAL"  
            elif recipe_container_mode == "INHERIT":
                df["recipe_container_name"] = container_env_name
            else:
                df["recipe_container_name"] = recipe_handle.get_settings().data["recipe"]["params"]["containerSelection"]["containerConf"]
        # SPARK
        if recipe_engine_type == "SPARK":
            sparkConfig = {}
            try:
                sparkConfig = recipe_handle.get_status().data["engineParams"]["sparkSQL"]["sparkConfig"]
            except:
                try:
                    sparkConfig = recipe_handle.get_settings().data["recipe"]["params"]["sparkConfig"]
                except:
                    pass
            df["recipe_spark_conf"] = sparkConfig.get("inheritConf", False)
            df["recipe_spark_mods"] = False
            if sparkConfig.get("conf", []):
                df["recipe_spark_mods"] = True
        # LLMS
        try:
            df["recipe_llm_mesh_id"] = recipe_handle.get_settings().get_json_payload()["llmId"]
        except:
            df["recipe_llm_mesh_id"] = False
    return df