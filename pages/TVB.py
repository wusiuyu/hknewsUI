# HK News DB Front End
# Select Box

# python -m streamlit run "C:\Projects\Project 034 Azure HK News\HK News UI\src\pages\hk01.py"

from io import StringIO
import time

import streamlit as st
import pandas as pd

from github_utilities import read_github_file


NEWS_DB_URL = f"https://api.github.com/repos/wusiuyu/hknews/contents/tvb_db.csv"
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
    st.write("**Browse news titles and expand for details:**")

    # Display news items using expanders
    if not media_df.empty:
        for _, row in media_df.iterrows():
            with st.expander(f"({row['date']}) {row['title']}"):
                st.write("---")
                st.subheader("News Details")
                st.write(f"**Title**: {row['title']}")
                st.write(f"**Publish**: {row['date']}")
                # HK01 Specific with Update Time
                st.write(f"**Update**: {row['last_update']}")
                st.write(f"**URL**: {row['url']}")
                st.write(f"**Content**:\n\n{row['news_content']}")
    else:
        st.warning("No data available. Please check the GitHub URL.")


if __name__ == "__main__":
    run()