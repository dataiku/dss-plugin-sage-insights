import streamlit as st
import altair as alt
import dataiku
from sage.src import dss_funcs

st.set_page_config(
    page_title="Dataiku Sage Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded"
)

alt.themes.enable("dark")

# Get Instance Name
client = dataiku.api_client()
st.session_state.instance_name = dss_funcs.get_dss_name(client)

# home
home = st.Page("pages/home.py", title="Home", icon=":material/login:", default=True)

# Administration
instance_checks = st.Page("pages/administration/instance_checks.py", title="Instance Checks")
os_vm = st.Page("pages/administration/os_vm.py", title="Operating System")

# Metrics and Graphs
projects = st.Page("pages/metrics_graphs/projects.py", title="Projects", icon=":material/dashboard:")
users = st.Page("pages/metrics_graphs/users.py", title="Users", icon=":material/dashboard:")
datasets = st.Page("pages/metrics_graphs/datasets.py", title="Datasets", icon=":material/dashboard:")
recipes = st.Page("pages/metrics_graphs/recipes.py", title="Recipes", icon=":material/dashboard:")
scenarios = st.Page("pages/metrics_graphs/scenarios.py", title="Scenarios", icon=":material/dashboard:")

# Debug
debug = st.Page("pages/debug.py", title="Debug")

# Navigation Panel
tree = {
    "Sage Insights": [home],
    "Administartion": [os_vm, instance_checks],
    "Metrics and Graphs": [users, projects, datasets, recipes, scenarios],
    "DEBUG": [debug]
}
if st.session_state.instance_name != "mazzei_designer":
    tree.pop("DEBUG")
pg = st.navigation(tree)
pg.run()