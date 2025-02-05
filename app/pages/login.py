"""
login.py
v0.2.0, 1/15/2025
Author: Alexander Netzley, anetzley@fredhutch.org
Ha Lab, Fred Hutchinson Cancer Research Center

This module provides the logic for the entry login page of the ichorCurate app.
"""

# Import packages
import streamlit as st

from src.ldap3_auth import authenticate

def display():
    st.title("Login Page")
    st.write("Please log in to continue.")

    # Input field for username
    username = st.text_input("Enter your username:", key="login_name")
    password = st.text_input("Enter your password:", type="password", key="login_password")

    # Login button
    if st.button("Login"):
        if authenticate(username, password):
            # Save username in session state
            st.session_state.username = username
            st.session_state.logged_in = True
            st.success(f"Welcome, {username}!")
            st.rerun()  # Refresh app to redirect after login
        else:
            st.error("Invalid username/password.")