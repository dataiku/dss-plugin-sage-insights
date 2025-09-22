import streamlit as st

# ------------------------------------------------------------------------------------
# Main function
def main(category, stock_insights, custom_insights, sidebar_categories = []):
    data_category = category.lower().replace(" ", "_")
    # Setup base sideba
    st.set_page_config(initial_sidebar_state="expanded")
    st.set_page_config(layout="wide")
    with st.sidebar:
        with st.container(border=True):
            genre = st.selectbox(
                label = "## Select an Insight",
                options = sidebar_categories,
                index = 0
            )

    # Display
    st.header(f"Dataiku {category}: {genre}")
    if genre == "LLM Applications":
        st.write("See Demo")
    else:
        st.write("Not there yet only had 45 minutes")