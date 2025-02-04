"""
app.py
v0.2.0, 1/15/2025
Author: Alexander Netzley, anetzley@fredhutch.org
Ha Lab, Fred Hutchinson Cancer Research Center

This module provides the wrapper function for running the ichorCurate app.
"""

# Import packages
import streamlit as st

# Import user modules
from pages.curation import display as curation_display
from pages.tracker_dashboard import display as tracker_dashboard_display
from pages.login import display as login_display
from pages.folder_selection import display as folder_selection_display
from src.utils import *

# Setting page formats
st.set_page_config(layout="wide")

# Title of the app
st.title('ichorCurate')

# Initialize session for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Redirect the user to the login page if they are not logged in
if not st.session_state.logged_in:
    login_display()

# Redirect the user to the folder selection page if they have not selected a folder
elif "selected_folder" not in st.session_state or "output_path" not in st.session_state:
    folder_selection_display()

else:
    # Initialize curated solutions in session state if it doesn't exist
    if "curated_solutions" not in st.session_state:
        st.session_state.curated_solutions = {}

    # Initialize visualization state in session state if it doesn't exist
    if "visualization" not in st.session_state:
        st.session_state.visualization = {}

    #Direct users to the tracker dashboard unless curation has been specified
    if "page" not in st.session_state:
        st.session_state.page = "Tracker Dashboard"

    # Sidebar navigation with automatic selection
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Menu", ["Tracker Dashboard", "Curation"], index=0 if st.session_state.page == "Tracker Dashboard" else 1)

    # Logout Button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        
        #Remap the user to the Tracker Dashboard to start
        st.session_state.page = "Tracker Dashboard"
        st.rerun()

    # Check and update the current page
    if page != st.session_state.page:
        st.session_state.page = page  # Sync sidebar selection with session state

    # Display the page
    if st.session_state.page == "Tracker Dashboard":
        tracker_dashboard_display()
    elif st.session_state.page == "Curation":
        curation_display()