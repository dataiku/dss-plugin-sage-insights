import streamlit as st
import importlib

from sage.src import dss_funcs
from sage.app_pages.layouts import layout_display
from sage.app_pages.layouts import layout_filter


def main(category, dss_objects, custom_dss_objects):
    data_category = category.lower()
    data_category = data_category.replace(" ", "_")

    # Load the INSIGHTS information
    display_data = []
    modules = {}
    if dss_objects:
        tmp_modules, tmp_display_data = dss_funcs.collect_display_data(dss_objects)
        modules = modules | tmp_modules
        display_data += tmp_display_data
    if custom_dss_objects:
        tmp_display_data, tmp_d = dss_funcs.collect_display_data(custom_dss_objects)
        modules = modules | tmp_modules
        display_data += tmp_display_data
    display_data = sorted(display_data)

    # initialize the module
    st.title(f"{category} Metadata")
    tab1, tab2, tab3, tab4 = st.tabs(["About", "Metrics", "Charts & Graphs", "Explore the Data"])
    with tab1:
        markdown = "##### Current list of Metrics, Charts and Graphs found\n"
        for key in display_data:
            module_name = modules[key][0]
            fp = modules[key][1]
            spec = importlib.util.spec_from_file_location(module_name, fp)
            try:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'main'):
                    results = module.main.__doc__
            except Exception as e:
                results = "No DOC string found."
            if not results:
                results = "No DOC string found."
            markdown += f"* **{key}:** {results}\n"
        st.write(markdown)
    with tab2:
        layout_display.body("metrics", modules, display_data)
    with tab3:
        layout_display.body("graphs", modules, display_data)
    with tab4:
        layout_filter.body(data_category, modules, display_data)
        