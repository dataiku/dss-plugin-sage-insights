# Sage Dashboard

* Author - Stephen Mazzei
* Email - <Stephen.Mazzei@dataiku.com>
* Version - 1.3.0

## Scope

This dashboard is designed to give Dataiku Admins insights into the DSS instance.

* DSS at a glance
* Individual objects, statistics, graphs
* Maintenance and performance reviews

## Installation

Due to the web application being built on Streamlit, installation requires a bit of dedicated code use. Hoping this changes in later DSS versions.

**TESTED ON VERSIONS:**
1. v13.5.5

##

1. Plugin
    1. Login as an admin account
    1. Migrate to plugins and install from GIT: https://github.com/mazzei-dataiku/sage.git
    1. Build the code-environment, no containers needed
    1. After the plugin is installed, switch to the plugin settings/paramets page and fill in the information
        1. "EXAMPLE"
        1. SAGE_DASHBOARD | HOST | API_KEY | SAGE_WORKER
        1. Fill out each host including the local host if you want to track the local host
1. Code Studios
    1. Create the template name `sage` # this name is important
    1. Setup K8s to run on
    1. Add the `Sage Dashboard - Streamlit` block
    1. Disable permissions for users
    1. Build
1. Create the Sage Dashboard project based off 1.4.2 information
    1. Go to Macros
    1. Filter on `sage insights`
    1. Run `Initialize Dashboard`
    1. Run `Initialize Workers`
    1. Switch to Code Studios page under the Code tab
        1. Click the checkbox and publish as a Web Application (No API for this)
        1. Start the Web Application (Auto-Start)
        1. Nothing may be available at first while the first day cycle needs to run to gather data