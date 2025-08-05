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
data_category = category.lower().replace(" ", "_")
df = dss_folder.read_base_data(f"/{data_category}/metadata.csv")

# Build the filters dictionary
filters = {}
filters["instance_name"] = {"label": "Select Instance Name", "values": df["instance_name"].unique().tolist()}
filters["enabled"] = {"label": "Select User Enablment", "values": df["enabled"].unique().tolist()}
filters["login"] = {"label": "Select DSS Login", "values": df["login"].unique().tolist()}

# Display
layout_main.main(category, stock_insights, custom_insights, filters)