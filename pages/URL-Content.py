# HK News UI, Scrape News Content using API

import requests
import streamlit as st
from urllib.parse import quote

# Function to clear text input
def clear_text():
    st.session_state["url"] = ""

def run():
    st.title("Media Scraper")
    st.text("Available: CRadio, Metro, MingPao, OnCC, SingTao")

    # Text input field with key for session state tracking
    url = st.text_input("Enter URL:", key="url")

    # Buttons for getting content and clearing input
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Get Content"):
            if url:
                url_encoded = quote(url)
                api_url = f"https://hknewsscrapeapi.azurewebsites.net/scrape/?url={url_encoded}"
                response = requests.get(api_url)
                if response.status_code == 200:
                    data = response.json()
                    st.write(f"**Formatted URL:** {data.get('url')}")
                    st.write(f"**Detected Media:** {data.get('media')}")
                    st.write(f"**Content**:\n\n{data.get('content')}")
                else:
                    st.error("Failed to retrieve media. Check the URL or API.")
            else:
                st.warning("Please enter a valid URL.")
    with col2:
        if st.button("Clear"):
            clear_text()

if __name__ == "__main__":
    run()
