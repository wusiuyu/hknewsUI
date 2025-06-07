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
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    # Original datetime string
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    chinese_weekday = weekdays[dt.weekday()]  # dt.weekday() gives index 0-6 (Monday-Sunday)
    # Format the date manually
    formatted_date = f"{dt.year}年{dt.month}月{dt.day}日（{chinese_weekday}）"
    formatted_time = f"香港時間{dt.hour}時{dt.minute:02d}分"  # Adjust to 21:00
    return formatted_date + "\n\n" + formatted_time


def content_add_space(content):
    return "\n\n".join(["  " + c for c in content.split("\n\n")])


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
    media_df = media_df[media_df["section"]=="Chi"]
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
                content += content_add_space(row['news_content'])
                content += "\n\n"
                content += "完"
                content += "\n\n"
                content += convert_hk_date(row['date'])
                st.write(f"**Content**:\n\n{content}")
    else:
        st.warning("No data available. Please check the GitHub URL.")


if __name__ == "__main__":
    run()