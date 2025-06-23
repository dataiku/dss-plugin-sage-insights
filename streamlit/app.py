import streamlit as st
import altair as alt

st.set_page_config(
    page_title="Dataiku Sage Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded"
)

alt.themes.enable("dark")

# home
home = st.Page("pages/home.py", title="Home", icon=":material/login:", default=True)

# Administration
instance_checks = st.Page("pages/administration/instance_checks.py", title="Instance Checks")

# Metrics and Graphs
projects = st.Page("pages/metrics_graphs/projects.py", title="Projects", icon=":material/dashboard:")
users = st.Page("pages/metrics_graphs/users.py", title="Users", icon=":material/dashboard:")
datasets = st.Page("pages/metrics_graphs/datasets.py", title="Datasets", icon=":material/dashboard:")
recipes = st.Page("pages/metrics_graphs/recipes.py", title="Recipes", icon=":material/dashboard:")
scenarios = st.Page("pages/metrics_graphs/scenarios.py", title="Scenarios", icon=":material/dashboard:")

# Debug
debug = st.Page("pages/debug.py", title="Debug")

# Navigation Panel
pg = st.navigation(
    {
        "Sage Insights": [home],
        "Administartion": [instance_checks],
        "Metrics and Graphs": [users, projects, datasets, recipes, scenarios],
        "DEBUG": [debug]
    }
)
pg.run()