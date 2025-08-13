# Main Import for layout
from sage.pages.insights import layout_main
from sage.src import dss_folder

# Try to import the modules for insights, normal and custom
try:
    from sage.insights import users as stock_insights       # Change this line
except:
    stock_insights = False

custom_insights = False

# Set the category and load the main layout
category = "Users"
layout_main.main(category, stock_insights, custom_insights)