from sage.streamlit.tab_pages.layouts import layout_main
try:
    from sage.insights import users as dss_objects # change this line
except:
    dss_objects = False

category = "Users" # change this line
layout_main.main(category, dss_objects)