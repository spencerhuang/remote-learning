import streamlit as st

# Simulate user authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None

# Dummy user database
users = {"admin": "password", "student1": "learn123"}

# Simulated course catalog with new course names
if "courses" not in st.session_state:
    st.session_state.courses = {
        "Scripts for Viral Video in Social Media": {"description": "Learn how to write engaging scripts that go viral!", "enrolled": set()},
        "Cinematography Basics Using Smartphone": {"description": "Master shooting techniques with just your phone.", "enrolled": set()},
        "Video Editing for Viral Video in Social Media": {"description": "Learn to edit videos that captivate audiences.", "enrolled": set()},
    }

# YouTube videos for each course
video_urls = {
    "Scripts for Viral Video in Social Media": "https://www.youtube.com/watch?v=xyz123",
    "Cinematography Basics Using Smartphone": "https://www.youtube.com/watch?v=abc456",
    "Video Editing for Viral Video in Social Media": "https://www.youtube.com/watch?v=def789",
}

# Ensure discussions persist with mock comments
if "discussions" not in st.session_state:
    st.session_state.discussions = {
        "Scripts for Viral Video in Social Media": [
            {"user": "Alice", "message": "I love how storytelling impacts engagement!"},
            {"user": "Bob", "message": "Short scripts with humor seem to perform best."}
        ],
        "Cinematography Basics Using Smartphone": [
            {"user": "Charlie", "message": "Lighting makes a huge difference, even with a phone!"},
            {"user": "Dana", "message": "Any tips for stabilizing shots without a gimbal?"}
        ],
        "Video Editing for Viral Video in Social Media": [
            {"user": "Eve", "message": "Transitions can really set the mood of the video."},
            {"user": "Frank", "message": "What’s the best free editing app for beginners?"}
        ],
    }

# ------------------------ AUTHENTICATION ------------------------
def login():
    st.sidebar.header("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username in users and users[username] == password:
            st.session_state.authenticated = True
            st.session_state.user = username
            st.sidebar.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.sidebar.error("Invalid credentials")

# ------------------------ COURSE CATALOG ------------------------
def show_courses():
    st.header("📚 Course Catalog")
    for course, details in st.session_state.courses.items():
        st.subheader(course)
        st.write(details["description"])
        if st.session_state.user in details["enrolled"]:
            st.success("✅ Enrolled")
        else:
            if st.button(f"Enroll in {course}", key=f"enroll_{course}"):
                st.session_state.courses[course]["enrolled"].add(st.session_state.user)
                st.success(f"✅ Enrolled in {course}")
                st.rerun()  # Force UI update

# ------------------------ DISCUSSION SECTION ------------------------
def show_discussion(course_name):
    st.subheader(f"💬 Discussion for {course_name}")

    # Show mock comments
    for msg in st.session_state.discussions[course_name]:
        st.write(f"👤 {msg['user']}: {msg['message']}")

    # Allow users to add new comments
    new_message = st.text_input("Type a message", key=f"msg_{course_name}")
    if st.button("Send", key=f"send_{course_name}"):
        if new_message:
            st.session_state.discussions[course_name].append({"user": st.session_state.user, "message": new_message})
            st.rerun()

# ------------------------ USER DASHBOARD ------------------------
def show_dashboard():
    st.header("📊 Your Learning Dashboard")
    enrolled_courses = [c for c in st.session_state.courses if st.session_state.user in st.session_state.courses[c]["enrolled"]]
    if enrolled_courses:
        for course in enrolled_courses:
            st.subheader(course)

            # Embed the YouTube video for the course
            if course in video_urls:
                st.video(video_urls[course])

            show_discussion(course)
    else:
        st.warning("You are not enrolled in any courses.")

# ------------------------ MAIN UI ------------------------
st.sidebar.title("🎓 Learning Platform")

if not st.session_state.authenticated:
    login()
else:
    st.sidebar.success(f"Logged in as {st.session_state.user}")
    page = st.sidebar.radio("Navigate", ["Course Catalog", "Dashboard", "Logout"])
    
    if page == "Course Catalog":
        show_courses()
    elif page == "Dashboard":
        show_dashboard()
    elif page == "Logout":
        st.session_state.authenticated = False
        st.session_state.user = None
        st.rerun()
