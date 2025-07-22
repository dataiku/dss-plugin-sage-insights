# -----------------------------------------------------------------------------
import sys
sys.dont_write_bytecode = True
    
import streamlit as st
import altair as alt
import dataiku


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
instance_checks = st.Page("app_pages/administration/instance_checks.py", title="Instance Checks")

# -----------------------------------------------------------------------------
# Operating System
disk_space = st.Page("app_pages/metrics_graphs/disk_space.py", title="Disk Space")

# -----------------------------------------------------------------------------
# Metrics and Graphs
projects  = st.Page("app_pages/metrics_graphs/projects.py",  title="Projects")
users     = st.Page("app_pages/metrics_graphs/users.py",     title="Users")
datasets  = st.Page("app_pages/metrics_graphs/datasets.py",  title="Datasets")
recipes   = st.Page("app_pages/metrics_graphs/recipes.py",   title="Recipes")
scenarios = st.Page("app_pages/metrics_graphs/scenarios.py", title="Scenarios")

# -----------------------------------------------------------------------------
# Navigation Panel
tree = {
    "Sage Insights":    [home],
    "Administration":   [instance_checks],
    "Operating System": [disk_space],
    "Dataiku Objects":  [users, projects, datasets, recipes, scenarios],
}

pg = st.navigation(tree, position="top")
with st.container(border=True):
    pg.run()
# -----------------------------------------------------------------------------
