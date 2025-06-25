import streamlit as st
import altair as alt
import dataiku
from sage.src import dss_funcs

# -----------------------------------------------------------------------------
# DSS Login Information
headers = st.context.headers
client = dataiku.api_client()
auth_info_browser = dataiku.api_client().get_auth_info_from_browser_headers(dict(headers))
user = auth_info_browser['authIdentifier']
st.session_state.debug = False
if user == 'admin':
    user = 'smazzei'
user_handle = client.get_user(login=user)
settings = user_handle.get_settings()
login = settings.settings['login'].lower()
login_display = settings.settings['displayName']
email = settings.settings['email']

client = dataiku.api_client()
st.session_state.instance_name = dss_funcs.get_dss_name(client)

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
# login / logout / home
def login():
    st.header(f" Welcome {login_display}")
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.session_state.login = login
        st.session_state.login_display = login_display
        st.session_state.email = email
        st.session_state.page = "dashboard"
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.page = None
        st.rerun()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

home = st.Page("tab_pages/home.py", title="Home", icon=":material/login:", default=True)

# -----------------------------------------------------------------------------
# Administration
instance_checks = st.Page("tab_pages/administration/instance_checks.py", title="Instance Checks")

# -----------------------------------------------------------------------------
# Operating System
disk_space = st.Page("tab_pages/metrics_graphs/disk_space.py", title="Disk Space")

# -----------------------------------------------------------------------------
# Metrics and Graphs
projects = st.Page("tab_pages/metrics_graphs/projects.py", title="Projects", icon=":material/dashboard:")
users = st.Page("tab_pages/metrics_graphs/users.py", title="Users", icon=":material/dashboard:")
datasets = st.Page("tab_pages/metrics_graphs/datasets.py", title="Datasets", icon=":material/dashboard:")
recipes = st.Page("tab_pages/metrics_graphs/recipes.py", title="Recipes", icon=":material/dashboard:")
scenarios = st.Page("tab_pages/metrics_graphs/scenarios.py", title="Scenarios", icon=":material/dashboard:")

# -----------------------------------------------------------------------------
# Debug
debug = st.Page("tab_pages/debug.py", title="Debug")

# -----------------------------------------------------------------------------
# Navigation Panel
tree = {
    "Sage Insights": [home],
    "Administartion": [instance_checks],
    "Operating System": [disk_space],
    "Dataiku Objects": [users, projects, datasets, recipes, scenarios],
    "Account": [logout],
    "DEBUG": [debug]
}
if st.session_state.instance_name != "mazzei_designer":
    tree.pop("DEBUG")

if st.session_state.logged_in:
    pg = st.navigation(tree)
else:
    pg = st.navigation([login])
pg.run()

# -----------------------------------------------------------------------------