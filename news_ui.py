# HK News DB Front End

# python -m streamlit run "C:\Projects\Project 033 HK News Reader\src\news_ui.py"

import streamlit as st
import pandas as pd

from io import StringIO

import time
from scraper_rthk import WAIT_TIME, NEWS_DB_URL
from scraper_rthk import read_github_file

def run():

    # Read News DB From GitHub
    try:
        rthk_csv = read_github_file(NEWS_DB_URL)          # Read News DB From GitHub
        time.sleep(WAIT_TIME)
        rthk_df = pd.read_csv(StringIO(rthk_csv))     # Convert Read DB into DF
    except:
        # When No DB from URL
        rthk_df = pd.DataFrame()
    
    # Filters
    rthk_df = rthk_df[rthk_df["section"] != "csport"]   # Remove China Sport Session

    # Add Time Filter, within 1 Day of Current Time

    st.set_page_config(
        page_title="HK News DB Front End",
        page_icon="👋",
    )

    st.write("# HK News DB 👋")

    # create a clear button in the sidebar
    if st.sidebar.button('Clear'):
        # clear the placeholder
        st.session_state.messages = []

    st.markdown(
        """
        HK News DB Platform built specifically for News Reader
        **👈 Select a demo from the sidebar** to see some examples
    """
    )

    # News DB 
    st.write(rthk_df)

if __name__ == "__main__":
    run()
