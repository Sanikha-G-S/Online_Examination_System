import streamlit as st

from auth import register_user
from auth import login_user

from database import create_tables

from exam_manager import *
from analytics import (
    get_statistics,
    get_leaderboard
)

from report_generator import (
    generate_result_pdf
)

create_tables()

st.set_page_config(
    page_title="Online Examination System",
    layout="wide"
)

# ------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

# ------------------

st.title("📝 Online Examination System")

# LOGIN AREA

if not st.session_state.logged_in:

    menu = st.sidebar.selectbox(
        "Menu",
        ["Login", "Register"]
    )

    # REGISTER

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
                    "Username Exists"
                )

    # LOGIN

    else:

        st.header("Login")

        username = st.text_input(
            "Username"
        )
        import sqlite3

        conn = sqlite3.connect("exam.db")
        cursor = conn.cursor()

        try:
           users = cursor.execute(
        "  SELECT username, role FROM users"
           ).fetchall()

          
        except Exception as e:
           st.error(str(e))

        conn.close()
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

# DASHBOARD

else:

    st.success(
        f"Welcome {st.session_state.username}"
    )
    
    # ADMIN PANEL

    if st.session_state.role == "admin":

        st.header("👨‍💼 Admin Dashboard")
        stats = get_statistics()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
        "Students",
        stats["students"]
   )

        col2.metric(
        "Average %",
        stats["average"]
   )

        col3.metric(
        "Highest %",
        stats["highest"]
   )

        col4.metric(
        "Lowest %",
        stats["lowest"]
)

        menu = st.sidebar.radio(
            "Admin Menu",
           [
            "Create Exam",
            "View Exams",
            "Add Question",
            "View Questions",
            "Leaderboard"
           ]
        )

        if menu == "Create Exam":

            exam_name = st.text_input(
                "Exam Name"
            )

            duration = st.number_input(
                "Duration",
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

        elif menu == "View Exams":

            exams = get_all_exams()

            for exam in exams:

                st.write(
                    f"ID: {exam[0]}"
                )

                st.write(
                    f"Exam: {exam[1]}"
                )

                st.write(
                    f"Duration: {exam[2]}"
                )

                st.divider()

        elif menu == "Add Question":

            exams = get_all_exams()

            if exams:

                exam_map = {
                    f"{e[0]} - {e[1]}": e[0]
                    for e in exams
                }

                selected = st.selectbox(
                    "Select Exam",
                    list(exam_map.keys())
                )

                exam_id = exam_map[selected]

                question = st.text_area(
                    "Question"
                )

                op1 = st.text_input(
                    "Option A"
                )

                op2 = st.text_input(
                    "Option B"
                )

                op3 = st.text_input(
                    "Option C"
                )

                op4 = st.text_input(
                    "Option D"
                )

                answer = st.selectbox(
                    "Correct Answer",
                    [op1, op2, op3, op4]
                )

                if st.button(
                    "Add Question"
                ):

                    add_question(
                        exam_id,
                        question,
                        op1,
                        op2,
                        op3,
                        op4,
                        answer
                    )

                    st.success(
                        "Question Added"
                    )

        elif menu == "View Questions":

            exams = get_all_exams()

            if exams:

                exam_map = {
                    f"{e[0]} - {e[1]}": e[0]
                    for e in exams
                }

                selected = st.selectbox(
                    "Select Exam",
                    list(exam_map.keys())
                )

                exam_id = exam_map[selected]

                questions = get_questions(
                    exam_id
                )

                for q in questions:

                    st.write(
                        f"Q: {q[2]}"
                    )

                    st.write(
                        f"A. {q[3]}"
                    )

                    st.write(
                        f"B. {q[4]}"
                    )

                    st.write(
                        f"C. {q[5]}"
                    )

                    st.write(
                        f"D. {q[6]}"
                    )

                    st.success(
                        f"Answer: {q[7]}"
                    )

                    st.divider()

        elif menu == "Leaderboard":

            st.subheader(
                "🏆 Leaderboard"
            )

            df = get_leaderboard()

            if len(df) > 0:

                st.dataframe(
                    df,
                    use_container_width=True
                )

            else:

                st.info(
                    "No Results Available"
                )  

    # STUDENT PANEL

    else:

        st.header("🎓 Student Dashboard")

        menu = st.sidebar.radio(
            "Student Menu",
            [
                "Take Exam",
                "My Results"
            ]
        )

        # TAKE EXAM

        if menu == "Take Exam":

            exams = get_all_exams()

            if exams:

                exam_map = {
                    f"{e[1]} ({e[2]} mins)": e[0]
                    for e in exams
                }

                selected_exam = st.selectbox(
                    "Choose Exam",
                    list(exam_map.keys())
                )

                exam_id = exam_map[selected_exam]

                questions = get_questions(
                    exam_id
                )

                answers = {}

                for q in questions:

                    answers[q[0]] = st.radio(
                        q[2],
                        [q[3], q[4], q[5], q[6]],
                        key=q[0]
                    )

                if st.button(
                    "Submit Exam"
                ):

                    score = 0

                    for q in questions:

                        if answers[q[0]] == q[7]:
                            score += 1

                    save_result(
                        st.session_state.username,
                        exam_id,
                        score,
                        len(questions)
                    )

                    st.success(
                        f"Score: {score}/{len(questions)}"
                    )

                    st.balloons()

        # RESULTS

        elif menu == "My Results":

            results = get_results(
                st.session_state.username
            )

            if results:

                for r in results:

                    st.write(
                        f"Exam ID: {r[2]}"
                    )

                    st.write(
                        f"Score: {r[3]}/{r[4]}"
                    )

                    st.divider()

            else:

                st.info(
                    "No Results Found"
                )

    # LOGOUT

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""

        st.rerun()