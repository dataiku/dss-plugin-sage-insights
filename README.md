# Sage Dashboard

* Author - Stephen Mazzei
* Email - Stephen.Mazzei@dataiku.com
* Version - 1.1

## Scope

This dashboard is designed to give Dataiku Admins insights into the DSS instance.

* DSS at a glance
* Individual objects, statistics, graphs
* Maintenance and performance reviews

## Installation

Due to the web application being built on Streamlit, installation requires a bit of dedicated code use. Hoping this changes in later DSS versions.

**(V13.5.5 and below)**

1. Login in as an `admin` permissioned account and open `Code Environments`
1. Dedicated Code Environment
    1. Create a new Code Environment template, use the label or `sage_dashbaord` use `PYTHON 3.11`
        1. Packages:
            ```python
            streamlit
            streamlit-aggrid
            altair
            urllib3
            matplotlib
            plotly
            ```
        1. No containers, Code Studios will buuild that
        1. Save and build local
1. Dedicated Code Studio 
    1. Create a new Code Studio template, use the label of `sage_dashboard`
    1. General
        1. Short Description: `**ADMIN USE ONLY**`
        1. Decscription: `This is a custom Streamlit Code Studio template for the Sag Dashbaord`
        1. Select the smallest K8S container, do not allow override
    1. Defnition
        1. Add Streamlit
        1. Code Env: `sage_dashboard` from the code environment we built
        1. Starting File: `__PROJECT_LIB_VERSIONED__/python/sage/streamlit/app.py`
        1. Settings Folder: `__PROJECT_LIB_VERSIONED__/python/sage/streamlit`
        1. Add Code Environment block --> `sage_dashbaord`
    1. Permissions
        1. Admin only
    1. Save and Build
1. Create a project called `Sage Dashboard`
    1. Pull the git repo into Library
        1. Import `https://github.com/dataiku/sage-dashboard.git`
        1. No login/pass
        1. Brach: `main`
        1. Path in git repo: `leave blank`
        1. Local Target Path: `python/sage`
    1. Create the streamlit web application
        1. Open Code Studios and create a new new studio for `sage_dashboard` using the Sage Code Studio template from before
        1. No need to start, simply go back to CS page
        1. Check the box, right panel `Publish` --> name `Sage Dashboard`
        1. Enable `Auto-Start`, which will save and run the application
        1. It will fail since no data has been gathered
    1. Create a new Scenario for data refresh
        1. Scenario Name: `Refresh Dashboard`
        1. Setup Run As as an Admin
        1. Run `DAILY at 4AM`
        1. Step 1
            1. Custom Python
            1. Name: `gather data`
            1. Custom code environment --> `sage_dashboard`
            1. Add the following code
                ```python
                from sage.src import main
                main.main()
                ```
        1. Step 2
            1. Restart webap
            1. Name: `Sage dashboard`
            1. Add dashbaord
        1. Save all and RUN