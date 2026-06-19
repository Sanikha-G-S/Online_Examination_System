import streamlit as st

from auth import register_user
from auth import login_user

from database import create_tables

from exam_manager import (
    create_exam,
    get_all_exams,
    add_question,
    get_questions
)

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

        username = st.text_input(
            "Username"
        )

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
                    "Username Exists"
                )

    else:

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
                    "Invalid Login"
                )

# ==========================
# DASHBOARDS
# ==========================

else:

    st.success(
        f"Welcome {st.session_state.username}"
    )

    # ----------------------
    # ADMIN
    # ----------------------

    if st.session_state.role == "admin":

        st.header("👨‍💼 Admin Dashboard")

        page = st.sidebar.radio(
            "Admin Menu",
            [
                "Create Exam",
                "View Exams",
                "Add Question",
                "View Questions"
            ]
        )

        # ------------------
        # CREATE EXAM
        # ------------------

        if page == "Create Exam":

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
                    "Exam Created"
                )

        # ------------------
        # VIEW EXAMS
        # ------------------

        elif page == "View Exams":

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
                        f"Duration : {exam[2]} mins"
                    )

                    st.divider()

            else:

                st.info(
                    "No Exams Found"
                )

        # ------------------
        # ADD QUESTION
        # ------------------

        elif page == "Add Question":

            exams = get_all_exams()

            if not exams:

                st.warning(
                    "Create an exam first"
                )

            else:

                exam_dict = {
                    f"{exam[0]} - {exam[1]}": exam[0]
                    for exam in exams
                }

                selected_exam = st.selectbox(
                    "Select Exam",
                    list(exam_dict.keys())
                )

                exam_id = exam_dict[
                    selected_exam
                ]

                question = st.text_area(
                    "Question"
                )

                option1 = st.text_input(
                    "Option A"
                )

                option2 = st.text_input(
                    "Option B"
                )

                option3 = st.text_input(
                    "Option C"
                )

                option4 = st.text_input(
                    "Option D"
                )

                answer = st.selectbox(
                    "Correct Answer",
                    [
                        option1,
                        option2,
                        option3,
                        option4
                    ]
                )

                if st.button(
                    "Add Question"
                ):

                    add_question(
                        exam_id,
                        question,
                        option1,
                        option2,
                        option3,
                        option4,
                        answer
                    )

                    st.success(
                        "Question Added"
                    )

        # ------------------
        # VIEW QUESTIONS
        # ------------------

        elif page == "View Questions":

            exams = get_all_exams()

            if exams:

                exam_dict = {
                    f"{exam[0]} - {exam[1]}": exam[0]
                    for exam in exams
                }

                selected_exam = st.selectbox(
                    "Select Exam",
                    list(exam_dict.keys())
                )

                exam_id = exam_dict[
                    selected_exam
                ]

                questions = get_questions(
                    exam_id
                )

                for q in questions:

                    st.write(
                        f"Q: {q[1]}"
                    )

                    st.write(
                        f"A) {q[2]}"
                    )

                    st.write(
                        f"B) {q[3]}"
                    )

                    st.write(
                        f"C) {q[4]}"
                    )

                    st.write(
                        f"D) {q[5]}"
                    )

                    st.success(
                        f"Answer: {q[6]}"
                    )

                    st.divider()

    # ----------------------
    # STUDENT
    # ----------------------

    else:

        st.header(
            "🎓 Student Dashboard"
        )

        st.info(
            "Exam Attempt Module Coming Next"
        )

    # ----------------------

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""

        st.rerun()