import streamlit as st
import requests
import pandas as pd
from streamlit_autorefresh import st_autorefresh

API_BASE_URL = "http://localhost:8080"  # Replace if your backend is hosted elsewhere

def fetch_uploaded_videos(token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/uploaded_videos", headers=headers)
        if response.status_code == 200:
            return True, response.json().get("videos", [])
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)

# ⏱ Auto-refresh every 30 seconds (30000 milliseconds)
st_autorefresh(interval=30 * 1000, key="video_status_polling")

# Page setup
st.title("📊 Uploaded Video Status")

if "access_token" not in st.session_state or not st.session_state.access_token:
    st.error("🔐 Please log in first.")
    st.stop()

ok, data = fetch_uploaded_videos(st.session_state.access_token)

if not ok:
    st.error(f"❌ Failed to fetch videos: {data}")
else:
    if not data:
        st.info("📭 No videos uploaded yet.")
    else:
        df = pd.DataFrame(data)
        df = df.rename(columns={
            "VideoID": "Video ID",
            "ClientID": "Client ID",
            "UploadTime": "Uploaded At",
            "Status": "Status",
            "FileKey": "File Key",
            "Bucket": "Bucket",
            "Strategy": "Strategy",
            "url": "Video URL"
        })
        st.dataframe(df, use_container_width=True)
