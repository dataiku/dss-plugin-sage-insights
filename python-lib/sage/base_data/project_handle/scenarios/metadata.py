import pandas as pd


def main(project_handle):
    cols = [
        "project_key", 
        "scenario_id",
        "scenario_name", 
        "scenario_type",
        "run_as_user",
        "is_active",
        "scenario_tags"
    ]

    df = pd.DataFrame(columns=cols)
    for scenario in project_handle.list_scenarios():
        scenario_handle = project_handle.get_scenario(scenario['id'])
        raw_settings    = scenario_handle.get_settings().get_raw()
        
        scenario_type   = raw_settings.get('type', None)
        scenario_runas  = raw_settings.get('runAsUser', None)
        if not scenario_owner:
            scenario_owner = raw_settings['versionTag']['lastModifiedBy']['login']
        sceanrio_active = raw_settings.get('active', False)
        scenario_id     = raw_settings.get('id', None)
        scenario_name   = raw_settings.get('name', None)
        scenario_tags   = raw_settings.get('tags', None)
        
        # Get additional information
        scenario_handle = project_handle.get_scenario(scenario_id=scenario_id)
        raw_settings = scenario_handle.get_settings().get_raw()
        try:
            version = scenario_handle.get_settings().get_raw()["versionTag"]
            version_num = version.get('versionNumber', None)
            version_num = version.get('tags', None)
            version_num = version.get('tags', None)
        
        # turn to dataframe
        d = [
            project_handle.project_key,
            scenario_id,
            scenario_name, 
            scenario_type,
            scenario_owner,
            sceanrio_active,
            scenario_tags
        ]
        tdf = pd.DataFrame([d], columns=cols)
        df = pd.concat([df, tdf], ignore_index=True)
    return df