import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Video Streaming SaaS",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar
st.sidebar.title("Navigation")
st.sidebar.write("Select a page from the options below:")

# Pages
page = st.sidebar.radio("Choose a page", ["Home", "📤 Upload", "📺 My Videos"])

# Home Page
if page == "Home":
    st.title("Welcome to the Video Streaming SaaS Platform")
    st.write("""
        This platform allows you to upload, transcode, and stream videos seamlessly. 
        Use the sidebar to navigate to different features such as uploading videos.
    """)
    st.image("https://via.placeholder.com/800x400?text=Video+Streaming", caption="Stream your videos with ease!")

# Redirect to Upload Page
elif page == "📤 Upload":
    st.write("Redirecting to upload page...")
    st.rerun()

# Redirect to My Videos Page (Can be implemented later)
elif page == "📺 My Videos":
    st.write("Here you can manage your uploaded videos.")
    st.write("Coming soon!")
