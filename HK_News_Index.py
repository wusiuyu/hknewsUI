# HK News Index Page

# python -m streamlit run "C:\Projects\Project 034 Azure HK News\HK News UI\src\HK_News_Index.py"

import streamlit as st


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# HK News 👋")

    # create a clear button in the sidebar
    if st.sidebar.button('Clear'):
        # clear the placeholder
        st.session_state.messages = []

    st.markdown(
        """
        HK News Page Index
        **👈 Select a Media from the sidebar** to see find News
    """
    )


if __name__ == "__main__":
    run()
