# I/O Methods for GitHub

import base64
import requests

import streamlit as st

TOKEN = st.secrets["TOKEN"]

def check_github_file_exists(url: str) -> bool:
    # Check if file in URL exist in Github
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.RequestException:
        return False


def write_github_file(csv, url):
    # Push a CSV file to Github
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.get(url)
    content = base64.b64encode(csv.encode()).decode()
    if check_github_file_exists(url):
        sha = read_github_json(url)["sha"]
        data = {"message": "Overwrite file via API", "sha": sha, "content": content}
    else:
        data = {"message": "Add file via API", "content": content}
    response = requests.put(url, json=data, headers=headers)
    return response


def read_github_file(url):
    # Read GitHub CSV as a Raw String
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.get(url=url, headers=headers)
    content = base64.b64decode(response.json()["content"])
    content = content.decode("UTF-8")
    return content


def read_github_json(url):
    # Read SHA of a GitHub file
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.get(url=url, headers=headers)
    return response.json()
