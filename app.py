import streamlit as st

from auth import register_user
from auth import login_user

st.set_page_config(
    page_title="Online Examination System"
)

# Session initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# --------------------------------

st.title("📝 Online Examination System")

if not st.session_state.logged_in:

    menu = st.sidebar.selectbox(
        "Menu",
        ["Login", "Register"]
    )

    # REGISTER

    if menu == "Register":

        st.subheader("Student Registration")

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

    # LOGIN

    if menu == "Login":

        st.subheader("Login")

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

                st.rerun()

            else:
                st.error(
                    "Invalid Credentials"
                )

else:

    st.success(
        f"Welcome {st.session_state.username}"
    )

    st.header("Student Dashboard")

    st.write(
        "Available Exams will appear here."
    )

    if st.button("Logout"):

        st.session_state.logged_in = False

        st.session_state.username = ""

        st.rerun()