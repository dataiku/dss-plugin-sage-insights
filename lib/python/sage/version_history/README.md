# Version History

## Alpha

1. Scope out context and design
1. Initial data gather
    1. Users - api.list_users, api.activity, dss_commits
    1. Projects - api.list_projects
    1. Datasets - Per project, api.list_datasets
    1. Recipes - Per project, api.list_recipes
    1. Scenarios - Per project, api.list_scenarios, get each scenario and its past run results (PASS, ABORT, FAILED)
1. Initial Steamlit Web Application
    1. Home page - Welcome
    1. Instance Level
        1. Users
            1. Basic intro graphs and metrics to get an idea scope
    1. Project
        1. Projects (though gathered at an instance level)
        1. Datasets, Scenarios, Recipes
            1. Scenarios just have boiler template place holders
            1. all others have just their main DF listed