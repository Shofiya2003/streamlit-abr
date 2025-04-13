import streamlit as st
import requests

API_BASE_URL = "http://localhost:8080"  # Replace with your Go backend URL

def login(username, password):
    try:
        response = requests.post(f"{API_BASE_URL}/api/v1/login", json={"username": username, "password": password})
        if response.status_code == 200:
            return True, response.json()  # Expecting: { "access_token": "...", "username": "..." }
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)

def signup(username, password):
    try:
        response = requests.post(f"{API_BASE_URL}/api/v1/register", json={"username": username, "password": password})
        if response.status_code == 201:
            return True, "Signup successful!"
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_data" not in st.session_state:
    st.session_state.user_data = None
if "access_token" not in st.session_state:
    st.session_state.access_token = None

st.title("🎥 SaaS Video Dashboard")

if st.session_state.logged_in:
    st.success(f"Welcome, {st.session_state.user_data.get('username', 'User')}!")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_data = None
        st.session_state.access_token = None
        st.rerun()

    # Example: Make an authorized request
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    video_response = requests.get(f"{API_BASE_URL}/api/v1/videos", headers=headers)
    if video_response.ok:
        st.write("📹 Your Videos", video_response.json())
    else:
        st.warning("Could not fetch videos.")

else:
    mode = st.radio("Choose an option", ["Login", "Signup"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button(mode):
        if mode == "Signup":
            ok, msg = signup(username, password)
        else:
            ok, msg = login(username, password)

        if ok:
            # Expect msg to be a dict: { "access_token": "...", "username": "..." }
            st.session_state.logged_in = True
            st.session_state.user_data = msg
            st.session_state.access_token = msg.get("access_token")
            st.rerun()
        else:
            st.error(msg)
