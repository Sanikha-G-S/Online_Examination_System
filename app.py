import streamlit as st
from auth import register_user

st.set_page_config(page_title="Online Examination System")

st.title("📝 Online Examination System")

menu = st.sidebar.selectbox(
    "Select Option",
    ["Register"]
)

if menu == "Register":

    st.subheader("Student Registration")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Register"):

        if register_user(username, password):
            st.success("Registration Successful")
        else:
            st.error("Username Already Exists")