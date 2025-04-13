import streamlit as st
import requests
import tempfile
import subprocess
import os

API_BASE_URL = "http://localhost:8080" 
def get_upload_url(filename, strategy, token):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "name": filename,
        "strategy": strategy,
        "bucket": "abr-raw",
        "file_type": "video/mp4"
    }
    response = requests.post(f"{API_BASE_URL}/api/v1/initialize_upload", json=payload, headers=headers)
    if response.status_code == 200:
        return True, response.json().get("upload_url")
    else:
        return False, response.text

def upload_video_to_s3(presigned_url, tmp_path):
    cmd = ["curl", "-X", "PUT", "-T", tmp_path, presigned_url]
    print(tmp_path)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        st.code(result.stdout + result.stderr)

        if result.returncode == 0:
            st.success("🎉 Video uploaded successfully via curl!")
        else:
            st.error("❌ Upload failed via curl.")
    except Exception as e:
        st.error(f"Error executing curl: {e}")

# Page UI
st.title("📤 Upload a Video")

if "access_token" not in st.session_state or not st.session_state.access_token:
    st.error("🔐 Please log in first.")
    st.stop()


uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])

if uploaded_file is not None:

    filename = uploaded_file.name
    print(filename)
    file_type = filename.split('.')[-1]

    # Ask for the strategy and bucket
    strategy = st.selectbox("Choose Strategy", ["single", "multi"])
    filename = st.text_input("Enter the filename to save (e.g., cat_video.mp4)")
    if st.button("Upload"):

        tmp_dir = "temp_uploads"
        os.makedirs(tmp_dir, exist_ok=True)
        tmp_path = os.path.join(tmp_dir, filename)

        with open(tmp_path, "wb") as f:
            f.write(uploaded_file.read())

        st.info(f"📁 File saved at: `{tmp_path}`")
        
        # Get the pre-signed URL
        ok, upload_url = get_upload_url(filename, strategy, st.session_state.access_token)
        if ok:
            # Upload the video to the pre-signed URL
            upload_video_to_s3(upload_url, tmp_path)

   
