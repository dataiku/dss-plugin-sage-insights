# Main Import for layout
from sage.pages.usage_patterns import layout_main
from sage.src import dss_folder

# Try to import the modules for insights, normal and custom
stock_insights = False
custom_insights = False

# Set the category and load the main layout
category = "GEN AI - LLM"
sidebar_categories = ["LLM Mesh", "LLM Applications"]
layout_main.main(category, stock_insights, custom_insights, sidebar_categories)