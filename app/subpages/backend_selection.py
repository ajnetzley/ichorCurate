"""
app.py
v1.0.0, 3/5/2025
Branch: external
Author: Alexander Netzley, anetzley@fredhutch.org
Ha Lab, Fred Hutchinson Cancer Research Center

This module provides the backend selection functionality to enable app persistence and collaboration.
"""

# Import packages
import streamlit as st

# Import user modules
from src.utils import save_backend_path, format_filepath, is_valid_backend, initialize_backend_folder

def display():
    st.title("Backend Selection")
    st.write("Select the backend folder location which will host the app metadata and enable persistence across users and sessions. If you are the first one in your organization to clone the repo you will need to select a new folder location. If someone else in your organization has already set up the backend location, enter that path here.")

    # Input field for username
    backend = format_filepath(st.text_input("Enter the backend folderpath:", key="login_name"))

    # Initializing error message
    error_message = ""
    
    if st.button("Hook Up to Backend"):
        # Check if the backend path exists
        is_valid, error_message = is_valid_backend(backend)

        if is_valid:
            # Save backend in session state
            st.session_state.backend = backend
            save_backend_path(backend)  # Save to YAML config file
            st.rerun()  # Refresh app to redirect

        elif error_message in ["Folder does not exist", "Config file does not exist", "Config file does not have correct formatting"]:
            st.session_state.new_backend_confirm = backend

        else:
            st.error("The backend path is invalid or the config file is unable to be loaded. Please enter a valid folder path.")

    if "new_backend_confirm" in st.session_state and st.session_state["new_backend_confirm"] == backend:
        st.error(f"The backend path has the error: ' {error_message} '. Would you like to create a new backend folder & config file at this location?")
        if st.button("Create New Backend"):
            initialize_backend_folder(backend)
            st.session_state.backend = backend
            save_backend_path(backend)
            del st.session_state["new_backend_confirm"]
            st.rerun()  # Refresh app to redirect

    
                    



