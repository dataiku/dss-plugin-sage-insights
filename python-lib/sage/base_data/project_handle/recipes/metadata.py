import pandas as pd
from sage.src.dss_funcs import get_nested_value


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
    
    project_r_env = project_handle.get_settings().settings["settings"]["codeEnvs"]["r"]["mode"]
    if project_r_env == "USE_BUILTIN_MODE":
        r_env_name = "USE_BUILTIN_MODE"
    elif project_r_env == "INHERIT":
        r_env_name = client_d["r_env_name"]
    else:
        r_env_name = project_handle.get_settings().settings["settings"]["codeEnvs"]["r"]["envName"]
        
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
    df = rename_and_move_first(project_handle, df, f"{prefix}projectKey", "project_key")