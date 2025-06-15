# HK News UI, Scrape News Content using API

import requests
import streamlit as st


def run():
    # Streamlit UI
    st.title("Media Scraper")
    url = st.text_input("Enter URL to scrape:")
    if st.button("Scrape Media"):
        if url:
            # Make request to FastAPI backend
            api_url = f"https://hknewsscrapeapi.azurewebsites.net/scrape/?url={url}"  # Adjust API URL if hosted elsewhere
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                st.write(f"**Formatted URL:** {data.get('url')}")
                st.write(f"**Detected Media:** {data.get('media')}")
            else:
                st.error("Failed to retrieve media. Check the URL or API.")
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    run()