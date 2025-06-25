import streamlit as st
import altair as alt
#import dataiku
#from sage.src import dss_funcs

# -----------------------------------------------------------------------------
# DSS Information
#client = dataiku.api_client()
st.session_state.instance_name = "mazzei_designer" #dss_funcs.get_dss_name(client)

# -----------------------------------------------------------------------------
# Setup streamlit configs
st.set_page_config(
    page_title="Dataiku Sage Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded"
)

alt.themes.enable("dark")

# -----------------------------------------------------------------------------
# Home
home = st.Page("app_pages/home.py", title="Home", default=True)

# -----------------------------------------------------------------------------
# Administration
#instance_checks = st.Page("app_pages/administration/instance_checks.py", title="Instance Checks")

# -----------------------------------------------------------------------------
# Operating System
#disk_space = st.Page("app_pages/metrics_graphs/disk_space.py", title="Disk Space")

# -----------------------------------------------------------------------------
# Metrics and Graphs
#projects  = st.Page("app_pages/metrics_graphs/projects.py",  title="Projects")
users     = st.Page("app_pages/metrics_graphs/users.py",     title="Users")
#datasets  = st.Page("app_pages/metrics_graphs/datasets.py",  title="Datasets")
#recipes   = st.Page("app_pages/metrics_graphs/recipes.py",   title="Recipes")
#scenarios = st.Page("app_pages/metrics_graphs/scenarios.py", title="Scenarios")

# -----------------------------------------------------------------------------
# Debug
#debug = st.Page("app_pages/debug.py", title="Debug")

# -----------------------------------------------------------------------------
# Navigation Panel
tree = {
    "Sage Insights":    [home],
    #"Administartion":   [instance_checks],
    #"Operating System": [disk_space],
    "Dataiku Objects":  [users], #, projects, datasets, recipes, scenarios],
    #"DEBUG":            [debug]
}
#if st.session_state.instance_name != "mazzei_designer":
#    tree.pop("DEBUG")

pg = st.navigation(tree)
pg.run()

# -----------------------------------------------------------------------------