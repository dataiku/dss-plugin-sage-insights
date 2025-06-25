import streamlit as st
from sage.streamlit.app_pages.layouts import layout_main
try:
    from sage.insights import users as dss_objects # change this line
except:
    dss_objects = False

category = "Users" # change this line
st.write("Level 1 testing: 11111111111")
layout_main.main(category, dss_objects)
#layout_main.main(category, dss_objects)