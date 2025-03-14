"""
app.py
v1.0.0, 3/14/2025
Branch: external
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
    username = st.text_input("Enter your username:", key="login_name")

    # Login button
    if st.button("Login"):
        # Save username in session state
        st.session_state.username = username
        st.session_state.logged_in = True
        st.success(f"Welcome, {username}!")
        st.rerun()  # Refresh app to redirect after login
