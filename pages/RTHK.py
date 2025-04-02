# RTHK News UI

# python -m streamlit run "C:\Projects\Project 034 Azure HK News\HK News UI\src\news_ui_02.py"

from io import StringIO
import time

import streamlit as st
import pandas as pd

from github_utilities import read_github_file


NEWS_DB_URL = f"https://api.github.com/repos/wusiuyu/hknews/contents/rthk_db.csv"
WAIT_TIME = 5

# Function to read data from GitHub and cache it
@st.cache_data
def fetch_news_data(url):
    try:
        media_csv = read_github_file(url)  # Fetch the CSV from GitHub
        time.sleep(WAIT_TIME)  # Simulating delay
        return pd.read_csv(StringIO(media_csv))
    except:
        return pd.DataFrame()  # Return empty DataFrame if there's an issue

def run():
    # Load the data once and cache the result
    media_df = fetch_news_data(NEWS_DB_URL)

    # Webpage layout
    st.title("News Titles")

    # Display static titles at the top
    st.write("**Select a news title to view its details:**")

    # Generate options for the selectbox
    if not media_df.empty:
        options = media_df.apply(lambda row: f"({row['date']}) {row['title']}", axis=1)
        selected_option = st.selectbox("Choose a title and time:", options=options)

        # Show the details at the bottom
        if selected_option:
            selected_title = selected_option.split(' )')[1].strip()
            selected_row = media_df[media_df['title'] == selected_title].iloc[0]
            st.write("---")  # Divider
            st.subheader("News Details")
            st.write(f"**Title**: {selected_row['title']}")
            st.write(f"**Time**: {selected_row['date']}")
            st.write(f"**URL**: {selected_row['url']}")
            st.write(f"**Content**:\n\n{selected_row['news_content']}")
    else:
        st.warning("No data available. Please check the GitHub URL.")
    
    with st.sidebar:
        if st.button("Refresh all News"):
            st.cache_data.clear()  # Clear cache globally
            st.success("All News Refreshed")


if __name__ == "__main__":
    run()