from sage.app_pages.layouts import layout_main
try:
    from sage.insights import scenarios as dss_objects # change this line
except:
    dss_objects = False
try:
    from sage_custom.insights import scenarios as custom_dss_objects
except:
    custom_dss_objects = False

category = "Scenarios" # change this line
layout_main.main(category, dss_objects, custom_dss_objects)