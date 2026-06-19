import streamlit as st

from auth import register_user
from auth import login_user

from database import create_tables

from exam_manager import create_exam
from exam_manager import get_all_exams

create_tables()

st.set_page_config(
    page_title="Online Examination System"
)

# ------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

# ------------------------

st.title("📝 Online Examination System")

# ==========================
# LOGIN / REGISTER
# ==========================

if not st.session_state.logged_in:

    menu = st.sidebar.selectbox(
        "Menu",
        ["Login", "Register"]
    )

    if menu == "Register":

        st.header("Student Registration")

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Register"):

            if register_user(
                username,
                password
            ):

                st.success(
                    "Registration Successful"
                )

            else:

                st.error(
                    "Username Already Exists"
                )

    elif menu == "Login":

        st.header("Login")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            user = login_user(
                username,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.username = user["username"]
                st.session_state.role = user["role"]

                st.rerun()

            else:

                st.error(
                    "Invalid Credentials"
                )

# ==========================
# DASHBOARDS
# ==========================

else:

    st.success(
        f"Welcome {st.session_state.username}"
    )

    st.write(
        f"Role : {st.session_state.role}"
    )

    # ----------------------
    # ADMIN DASHBOARD
    # ----------------------

    if st.session_state.role == "admin":

        st.header("👨‍💼 Admin Dashboard")

        page = st.sidebar.radio(
            "Admin Menu",
            [
                "Create Exam",
                "View Exams"
            ]
        )

        # CREATE EXAM

        if page == "Create Exam":

            st.subheader("Create New Exam")

            exam_name = st.text_input(
                "Exam Name"
            )

            duration = st.number_input(
                "Duration (minutes)",
                min_value=1
            )

            if st.button(
                "Create Exam"
            ):

                create_exam(
                    exam_name,
                    duration
                )

                st.success(
                    "Exam Created Successfully"
                )

        # VIEW EXAMS

        elif page == "View Exams":

            st.subheader(
                "Available Exams"
            )

            exams = get_all_exams()

            if exams:

                for exam in exams:

                    st.write(
                        f"ID : {exam[0]}"
                    )

                    st.write(
                        f"Exam : {exam[1]}"
                    )

                    st.write(
                        f"Duration : {exam[2]} Minutes"
                    )

                    st.divider()

            else:

                st.info(
                    "No Exams Created"
                )

    # ----------------------
    # STUDENT DASHBOARD
    # ----------------------

    else:

        st.header(
            "🎓 Student Dashboard"
        )

        st.info(
            "Exam Module Coming Next"
        )

    # ----------------------

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""

        st.rerun()