# HK News UI, Scrape News Content using API

import requests
import streamlit as st
from urllib.parse import quote

def run():
    # Streamlit UI
    st.title("Media Scraper")
    st.text("Available: CRadio, Metro, MingPao, OnCC, SingTao")

    # Create a placeholder for the text input
    input_placeholder = st.empty()

    # Initialize session state for URL input
    if "url" not in st.session_state:
        st.session_state.url = ""

    # Display the text input field
    url = input_placeholder.text_input("Enter URL to scrape:", st.session_state.url)

    # Buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        get_content = st.button("Get Content")
    with col2:
        clear_text = st.button("Clear")

    # Clear button functionality
    if clear_text:
        st.session_state.url = ""  # Reset session state
        input_placeholder.empty()  # Clear the input field by recreating it

    # Get Content button functionality
    if get_content:
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