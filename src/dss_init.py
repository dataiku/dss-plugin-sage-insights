def get_dss_commits(client):
    # Check for project
    if "SAGE_WORKER" not in client.list_project_keys():
        project_handle = client.create_project(project_key="SAGE_WORKER", name="SAGE WORKER", owner="admin")
    else:
        project_handle = client.get_project(project_key="SAGE_WORKER")
    # Check for dataset
    project_handle = client.get_project("SAGE_WORKER")
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
    return dataset


if __name__ == "__main__":
    main()