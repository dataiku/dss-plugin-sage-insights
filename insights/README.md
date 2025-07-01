# How to build your own insights

## Exploration

1. Open a Jupyter Notebook
1. Copy in the boiler template code for either `graphs-example.py` or `metrics-example.py`. You can unnest the block keeping in:
    1. Imports
    1. Data Read
    1. `code block for testing`
    1. Populating the data structure dictionary
1. Once you have the data smoothed to how you initially prepare to think about it
    1. Create a file under the sub-section: Exmple `projects/metrics-new_metric.py`
    1. Copy the code into the file from the notebook, aligning it back into the deffinition block
    1. Save / Restart the web application (Data is dynamic, insights are not)
    1. In a second windows tab, open the Dashboard and explore the new insight. If it doesn't work correctly, you can adjust and restart the web application.

## Types of structures

1. Streamlit BAR_CHART
1. Streamlit METRIC