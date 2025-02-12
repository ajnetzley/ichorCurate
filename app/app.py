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
from pages.projects_overview import display as projects_overview_display
from src.utils import *

# Setting page formats
st.set_page_config(layout="wide")

# Title of the app
st.title('ichorCurate')

# Map to backend location
st.session_state.backend = "/fh/fast/ha_g/user/anetzley/ichorCurate-backend"

# Initialize session for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Redirect the user to the login page if they are not logged in
if not st.session_state.logged_in:
    login_display()

# Redirect the user to the projects overview page if they are logged in and have not selected a project
elif ("selected_project" not in st.session_state or st.session_state.selected_project is None) and st.session_state.logged_in == True:
    projects_overview_display()

# Redirect the user to the folder selection page if they have not selected a folder
elif ("selected_folder" not in st.session_state or "output_path" not in st.session_state) and st.session_state.logged_in == True:
    folder_selection_display()

else:
    # Initialize curated solutions in session state if it doesn't exist
    if "curated_solutions" not in st.session_state[st.session_state.selected_project]: 
        st.session_state[st.session_state.selected_project]["curated_solutions"] = {}

    # Initialize visualization state in session state if it doesn't exist
    if "visualization" not in st.session_state[st.session_state.selected_project]:
        st.session_state[st.session_state.selected_project]["visualization"] = {}

    #Direct users to the tracker dashboard unless curation has been specified
    if "page" not in st.session_state:
        st.session_state.page = "Tracker Dashboard"

    # Logout Button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        
        #Remap the user to the Tracker Dashboard to start
        st.session_state.page = "Tracker Dashboard"
        st.rerun()

    # Project Reselection
    if st.session_state.selected_project:
        st.sidebar.subheader("Project Selection")
        st.sidebar.write(f"You are currently working on {st.session_state.selected_project}.")
        if st.sidebar.button("Select New Project"):
            st.session_state.selected_project = None
            st.session_state.selected_folder = None
            st.session_state.output_path = None
            #Remap the user to the Tracker Dashboard to start
            st.session_state.page = "Tracker Dashboard"
            st.rerun()

    # Display the page
    if st.session_state.page == "Tracker Dashboard" and st.session_state.logged_in == True:
        tracker_dashboard_display()
    elif st.session_state.page == "Curation" and st.session_state.logged_in == True:
        curation_display()