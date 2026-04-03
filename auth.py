# import streamlit as st

# def login():
#     if "authenticated" not in st.session_state:
#         st.session_state.authenticated = False

#     if not st.session_state.authenticated:
#         st.title("ResolveIQ Login")

#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")

#         if st.button("Login"):
#             if username == "admin" and password == "resolve123":
#                 st.session_state.authenticated = True
#                 st.success("Login Successful")
#             else:
#                 st.error("Invalid credentials")

#         st.stop()
import streamlit as st
from database import add_user, authenticate

def login():

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "username" not in st.session_state:
        st.session_state.username = None

    # If already logged in → skip login screen
    if st.session_state.authenticated:
        return

    st.title("🔐 ResolveIQ Login")

    menu = ["Login", "Sign Up"]
    choice = st.radio("", menu, horizontal=True)

    if choice == "Login":

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = authenticate(username, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid credentials")

    elif choice == "Sign Up":

        new_user = st.text_input("Create Username")
        new_pass = st.text_input("Create Password", type="password")

        if st.button("Create Account"):
            if add_user(new_user, new_pass):
                st.success("Account created! Please login.")
            else:
                st.error("Username already exists.")

    st.stop()  # 🚨 IMPORTANT — stops app until login