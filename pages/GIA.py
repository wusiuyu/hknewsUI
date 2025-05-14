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
    # Set locale for Chinese formatting (optional, depending on the environment)
    locale.setlocale(locale.LC_TIME, "zh_HK.UTF-8")
    # Original datetime string
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    # Format output with weekday and adjusted time
    formatted_date = dt.strftime("%Y年%-m月%-d日（%A）")  # Format with full weekday name
    formatted_time = f"香港時間{dt.hour}時{dt.minute:02d}分"
    return formatted_date + "\n\n" + formatted_time



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
                st.write(f"**URL**: {row['url']}")
                content = row["title"]
                content += "\n\n"
                content += "＊" * (len(row["title"]) + 1)
                content += "\n\n"
                content += row['news_content']
                content += "\n\n"
                content += convert_hk_date(row['date'])
                st.write(f"**Content**:\n\n{content}")
    else:
        st.warning("No data available. Please check the GitHub URL.")


if __name__ == "__main__":
    run()