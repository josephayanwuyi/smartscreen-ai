import streamlit as st
import sqlite3
from modules.services.db_service import DB_NAME, transfer_guest_data, create_user

def verify_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT region FROM users WHERE username=? AND password=?", (username, password))
    user_data = c.fetchone()
    conn.close()
    return user_data

def login():
    st.header("🔐 Authentication")
    
    # Create toggle tabs for Login vs Register
    tab_login, tab_register = st.tabs(["Existing User", "Create Account"])

    # --- LOGIN FORM ---
    with tab_login:
        st.subheader("Login")
        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            user_info = verify_user(login_user, login_pass)
            if user_info:
                st.session_state.user = login_user
                st.session_state.region = user_info[0]
                
                # Claim guest history
                transfer_guest_data(st.session_state.guest_id, login_user)
                
                st.success(f"Welcome back, {login_user}!")
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")

    # --- REGISTRATION FORM ---
    with tab_register:
        st.subheader("Register")
        new_user = st.text_input("Choose Username", key="reg_user")
        new_pass = st.text_input("Choose Password", type="password", key="reg_pass")
        region = st.selectbox(
            "Select Your Region", 
            ["Africa", "Europe", "Asia", "Americas", "Oceania"],
            key="reg_region"
        )
        
        if st.button("Register Now"):
            if new_user and new_pass:
                if create_user(new_user, new_pass, region):
                    st.success("Account created successfully! Now switch to the 'Existing User' tab to login.")
                else:
                    st.error("That username is already taken. Please pick another.")
            else:
                st.warning("Please fill out all fields to continue.")