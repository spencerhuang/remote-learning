import streamlit as st
import pandas as pd

# Simulate user authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None

# Dummy user database
users = {"admin": "password", "student1": "learn123"}

# Simulate a course database
courses = {
    "Python for Beginners": {"description": "Learn Python from scratch!", "enrolled": []},
    "AI Ethics": {"description": "Understand AI's ethical implications.", "enrolled": []},
    "Product Management 101": {"description": "Master the fundamentals of PM.", "enrolled": []},
}

# Dummy discussion storage
if "discussions" not in st.session_state:
    st.session_state.discussions = {course: [] for course in courses}

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
        else:
            st.sidebar.error("Invalid credentials")

# ------------------------ COURSE CATALOG ------------------------
def show_courses():
    st.header("📚 Course Catalog")
    for course, details in courses.items():
        st.subheader(course)
        st.write(details["description"])
        if st.session_state.user in details["enrolled"]:
            st.success("✅ Enrolled")
        else:
            if st.button(f"Enroll in {course}", key=course):
                courses[course]["enrolled"].append(st.session_state.user)
                st.success(f"Enrolled in {course}")

# ------------------------ DISCUSSION SECTION ------------------------
def show_discussion(course_name):
    st.subheader(f"💬 Discussion for {course_name}")
    for msg in st.session_state.discussions[course_name]:
        st.write(f"👤 {msg['user']}: {msg['message']}")
    new_message = st.text_input("Type a message", key=f"msg_{course_name}")
    if st.button("Send", key=f"send_{course_name}"):
        if new_message:
            st.session_state.discussions[course_name].append({"user": st.session_state.user, "message": new_message})
            st.experimental_rerun()

# ------------------------ USER DASHBOARD ------------------------
def show_dashboard():
    st.header("📊 Your Learning Dashboard")
    enrolled_courses = [c for c in courses if st.session_state.user in courses[c]["enrolled"]]
    if enrolled_courses:
        for course in enrolled_courses:
            st.subheader(course)
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
        st.experimental_rerun()
