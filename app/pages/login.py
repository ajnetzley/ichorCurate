"""
login.py
v0.2.0, 1/15/2025
Author: Alexander Netzley, anetzley@fredhutch.org
Ha Lab, Fred Hutchinson Cancer Research Center

This module provides the logic for the entry login page of the ichorCurate app.
"""

# Import packages
import streamlit as st

def display():
    st.title("Login Page")
    st.write("Please log in to continue.")

    # Input field for username
    username = st.text_input("Enter your name:", key="login_name")

    # Login button
    if st.button("Login"):
        if username:
            # Save username in session state
            st.session_state.username = username
            st.session_state.logged_in = True
            st.success(f"Welcome, {username}!")
            st.rerun()  # Refresh app to redirect after login
        else:
            st.error("Please enter your name.")
