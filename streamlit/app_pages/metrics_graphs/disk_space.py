from sage.streamlit.tab_pages.layouts import layout_main
try:
    from sage.insights import disk_space as dss_objects # change this line
except:
    dss_objects = False

category = "Disk Space" # change this line
layout_main.main(category, dss_objects)