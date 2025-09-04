import pandas as pd


def main(project_handle, client_d = {}):
    dfs = []
    for scenario in project_handle.list_scenarios():
        d = {"project_key": project_handle.project_key}
        
        # Poll Data
        scenario_handle = project_handle.get_scenario(scenario['id'])
        raw_settings    = scenario_handle.get_settings().get_raw()
        d["scenario_type"]   = raw_settings.get('type', None)
        d["scenario_run_as"] = raw_settings.get('runAsUser', None)
        d["scenario_effective_run_as"] = raw_settings.effective_run_as
        d["sceanrio_active"] = raw_settings.get('active', False)
        d["scenario_id"]     = raw_settings.get('id', None)
        d["scenario_name"]   = raw_settings.get('name', None)
        d["scenario_tags"]   = raw_settings.get('tags', None)
        version = scenario_handle.get_settings().get_raw()["versionTag"]
        d["scenario_version_num"] = version.get('versionNumber', None)
        d["scenario_last_mod_by"] = version["lastModifiedBy"].get("login", None)
        d["scenario_last_mod_dt"] = version.get('lastModifiedOn', None)
        d["scenario_last_mod_dt"] = pd.to_datetime(d["scenario_last_mod_dt"], unit="ms")
        
        # turn to dataframe
        dfs.append(pd.DataFrame([d]))
    df = pd.concat(dfs, ignore_index=True)
    return df