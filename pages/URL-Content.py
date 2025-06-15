# HK News UI, Scrape News Content using API

import requests
import streamlit as st
from urllib.parse import quote

def run():
    # Streamlit UI
    st.title("Media Scraper")
    st.text("Available: CRadio, HK01, Metro, MingPao, OnCC, SingTao")

    # Text input field
    url = st.text_input("Enter URL to scrape:")

    # Get Content button functionality
    if st.button("Get Content"):
        if url:
            url = quote(url)
            api_url = f"https://hknewsscrapeapi.azurewebsites.net/scrape/?url={url}"  # Adjust API URL if hosted elsewhere
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

if __name__ == "__main__":
    run()
