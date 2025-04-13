import streamlit as st
import requests

API_BASE_URL = "http://localhost:8080" 
def get_upload_url(filename, strategy, token):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "filename": filename,
        "strategy": strategy,
        "bucket": "abr-raw",
        "file_type": "video/mp4"
    }
    response = requests.post(f"{API_BASE_URL}/api/v1/initialize_upload", json=payload, headers=headers)
    if response.status_code == 200:
        return True, response.json().get("upload_url")
    else:
        return False, response.text

def upload_video_to_s3(upload_url, video_file):
    try:
        # Send a PUT request to upload the file
        response = requests.put(upload_url, files={"file": video_file})
        if response.status_code == 200:
            st.success("Video uploaded successfully!")
        else:
            st.error(f"Failed to upload video. Status code: {response.status_code}")
            st.error(response.text)
        print(response)
        print(response.json())
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Page UI
st.title("📤 Upload a Video")

if "access_token" not in st.session_state or not st.session_state.access_token:
    st.error("🔐 Please log in first.")
    st.stop()


uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # Get filename and file type
    filename = uploaded_file.name
    file_type = filename.split('.')[-1]  # Extract file type

    # Ask for the strategy and bucket
    strategy = st.selectbox("Choose Strategy", ["single", "multi"])

    if st.button("Upload"):
        # Get the pre-signed URL
        ok, upload_url = get_upload_url(filename, strategy, st.session_state.access_token)

        if ok:
            # Upload the video to the pre-signed URL
            upload_video_to_s3(upload_url, uploaded_file)
