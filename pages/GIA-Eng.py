# HK News DB Front End
# Select Box

# python -m streamlit run "C:\Projects\Project 034 Azure HK News\HK News UI\src\pages\hk01.py"

from datetime import datetime
import locale
from io import StringIO
import time


import streamlit as st
import pandas as pd

from github_utilities import read_github_file


NEWS_DB_URL = f"https://api.github.com/repos/wusiuyu/hknews/contents/gia_db.csv"
WAIT_TIME = 5

def convert_hk_date(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    # Original datetime string
    formatted_date = f"Ends/{dt.strftime('%A, %B %d, %Y')}  \nIssued at HKT {dt.strftime('%H:%M')}"
    return formatted_date


def content_add_space(content):
    return "\n\n".join(["　　" + c for c in content.split("\n\n")])


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
    media_df = media_df[media_df["section"]=="Eng"]
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
                st.write(f"**URL**: {row['url']}")
                st.write(f"**Content**:")
                title = row["title"]
                title += "\n\n"
                st.write(title)
                breakline = "*" * min((len(row["title"]) + 1), 85)
                st.text(breakline)
                content = "\n\n"
                content += content_add_space(row['news_content'])
                content += "\n\n"
                content += convert_hk_date(row['date'])
                content += "\n\n"
                content += "N" * 4
                # st.write(f"**Content**:\n\n{content}")
                st.write(f"****:\n\n{content}")
    else:
        st.warning("No data available. Please check the GitHub URL.")


if __name__ == "__main__":
    run()