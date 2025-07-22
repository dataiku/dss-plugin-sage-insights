from sage.app_pages.layouts import layout_main
try:
    from sage.insights import projects as dss_objects # change this line
except:
    dss_objects = False
try:
    from sage_custom.insights import projects as custom_dss_objects
except:
    custom_dss_objects = False

category = "Projects" # change this line
layout_main.main(category, dss_objects, custom_dss_objects)