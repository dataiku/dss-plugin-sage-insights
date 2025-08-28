import tomllib
import json


worker_scenarios = """
[default]
trigger = '{"type": "temporal", "name": "Time-based", "delay": 5, "active": true, "params": {"repeatFrequency": 1, "frequency": "Daily", "startingFrom": "2025-07-16", "daysOfWeek": ["Wednesday"], "monthlyRunOn": "ON_THE_DAY", "minute": 0, "hour": 17, "timezone": "Canada/Eastern"}}'
step = '{"type": "runnable", "name": "run_macro", "enabled": true, "alwaysShowComment": false, "runConditionType": "RUN_IF_STATUS_MATCH", "runConditionStatuses": ["SUCCESS", "WARNING"], "runConditionExpression": "", "resetScenarioStatus": false, "delayBetweenRetries": 10, "maxRetriesOnFail": 0, "params": {"runnableType": "REPLACE_MACRO_HERE",   "config": {}, "adminConfig": {}, "proceedOnFailure": false}}'

[data_gather_instance]
macro = "pyrunnable_sage_data-gather-instance"

[data_gather_project]
macro = "pyrunnable_sage_data-gather-project"

[data_gather_audit_logs]
macro = "pyrunnable_sage_data-gather-audit-user-login"

[data_gather_diskspace]
macro = "pyrunnable_sage_data-gather-diskspace"

[data_gather_filesystem]
macro = "pyrunnable_sage_data-gather-filesystem"
"""

dashboard_scenarios = """
[default]
trigger = '{"type": "temporal", "name": "Time-based", "delay": 5, "active": true, "params": {"repeatFrequency": 1, "frequency": "Daily", "startingFrom": "2025-07-16", "daysOfWeek": ["Wednesday"], "monthlyRunOn": "ON_THE_DAY", "minute": 0, "hour": 18, "timezone": "Canada/Eastern"}}'
step = '{"type": "runnable", "name": "run_macro", "enabled": true, "alwaysShowComment": false, "runConditionType": "RUN_IF_STATUS_MATCH", "runConditionStatuses": ["SUCCESS", "WARNING"], "runConditionExpression": "", "resetScenarioStatus": false, "delayBetweenRetries": 10, "maxRetriesOnFail": 0, "params": {"runnableType": "REPLACE_MACRO_HERE",   "config": {}, "adminConfig": {}, "proceedOnFailure": false}}'

[refresh_base_data]
macro = "pyrunnable_sage_data-smoothing-base"

[addon_base_data]
macro = "pyrunnable_sage_data-gather-partition-history"
"""

def update_plugin_config(self, plugin_handle):
    settings = plugin_handle.get_settings()
    settings.settings["config"]["sage_project_key"] = self.sage_project_key
    settings.settings["config"]["sage_project_api"] = self.sage_project_api
    settings.settings["config"]["sage_project_url"] = self.sage_project_url
    settings.settings["config"]["sage_worker_key"]  = self.sage_worker_key
    settings.settings["config"]["sage_folder_connection"] = self.sage_folder_connection
    settings.settings["config"]["sage_repo_url"]    = self.sage_repo_url
    settings.settings["config"]["sage_repo_branch"] = self.sage_folder_connection 
    settings.settings["codeEnvName"] = "plugin_sage_managed"
    settings.save()
    return

    
def install_plugin(self, remote_client):
    # Only install if not found
    sage_found = False
    for plugin in remote_client.list_plugins():
        if plugin["id"] == "sage":
            sage_found = True
    if sage_found:
        if self.update_github:
            plugin_handle = remote_client.get_plugin(plugin_id="sage")
            plugin_handle.update_from_git(repository_url=self.sage_repo_url, checkout=self.sage_repo_branch)
            update_plugin_config(self, plugin_handle)
        return
    
    # install the plugin
    plugin_install = remote_client.install_plugin_from_git(
        repository_url=self.sage_repo_url, checkout=self.sage_repo_branch, subpath=None
    )
    r = plugin_install.wait_for_result()
    r = plugin_install.get_result()
    if r["messages"]["warning"] or r["messages"]["error"] or r["messages"]["fatal"]:
        raise Exception(r["messages"]["messages"])
    
    # connect to the plugin handle
    plugin_handle = remote_client.get_plugin(plugin_id="sage")
    
    # create the code-env
    code_env = plugin_handle.create_code_env()
    r = code_env.wait_for_result()
    r = code_env.get_result()
    if r["messages"]["warning"] or r["messages"]["error"] or r["messages"]["fatal"]:
        raise Exception(r["messages"]["messages"])
        
    update_plugin_config(self, plugin_handle)
    
    return


def create_worker(client, sage_worker_key):
    if sage_worker_key not in client.list_project_keys():
        project_handle = client.create_project(project_key=sage_worker_key, name=sage_worker_key, owner="admin")
    else:
        project_handle = client.get_project(project_key=sage_worker_key)
    return project_handle


def get_dss_commits(project_handle):
    dataset = project_handle.get_dataset("dss_commits")
    if not dataset.exists():
        dataset = project_handle.create_dataset(
            dataset_name = "dss_commits",
            type = "StatsDB",
            params = {
                'view': 'COMMITS',
                'orderByDate': False,
                'clusterTasks': {},
                'commits': {},
                'jobs': {},
                'scenarioRuns': {},
                'flowActions': {}
            }
        )
        schema = {
            "columns": [
                {"name": "project_key", "type": "string"},
                {"name": "commit_id", "type": "string"},
                {"name": "author", "type": "string"},
                {"name": "timestamp", "type": "bigint"},
                {"name": "added_files", "type": "int"},
                {"name": "added_lines", "type": "int"},
                {"name": "removed_files", "type": "int"},
                {"name": "removed_lines", "type": "int"},
                {"name": "changed_files", "type": "int"},
            ],
            "userModified": True,
        }
        r = dataset.set_schema(schema=schema)
    return


def create_scenarios(project_handle, location, run_as_user):
    # Clear out any old
    for scenario in project_handle.list_scenarios():
        if "data_gather_" in scenario["name"]:
            scenario_handle = project_handle.get_scenario(scenario["id"])
            r = scenario_handle.delete()
    
    # Create the scenarios
    if location ==  "WORKER":
        macros = tomllib.loads(worker_scenarios)
    else:
        macros = tomllib.loads(dashboard_scenarios)
    for key in macros:
        # skip default
        if key == "default":
            continue
        # rebase and setup macro in step
        trigger = json.loads(macros["default"]["trigger"])
        step = json.loads(macros["default"]["step"])
        step["params"]["runnableType"] = macros[key]["macro"]
        # create or connect to scenario
        try:
            scenario_handle = project_handle.get_scenario(scenario_id=key)
            settings = scenario_handle.get_settings()
        except:
            scenario_handle = project_handle.create_scenario(scenario_name=key, type="step_based")
            settings = scenario_handle.get_settings()
        # Run As User
        settings.data["runAsUser"] = run_as_user
        # Trigger
        del settings.raw_triggers[:]
        settings.raw_triggers.append(trigger)
        # Steps
        del settings.raw_steps[:]
        settings.raw_steps.append(step)
        # Save
        settings.active = True
        settings.save()
        # RUN
        if location ==  "WORKER":
            run = scenario_handle.run()
    return