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
        data = scenario_handle.get_settings().get_raw()
        scenario_type = data.get('type', None)
        scenario_owner = data.get('runAsUser', None)
        if not scenario_owner:
            scenario_owner = data['versionTag']['lastModifiedBy']['login']
        sceanrio_active = data.get('active', False)
        scenario_id = data.get('id', None)
        scenario_name = data.get('name', None)
        scenario_tags = data.get('tags', None)
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