"""
login.py
v0.1.0, 12/2/2024
Author: Alexander Netzley, anetzley@fredhutch.org
Ha Lab, Fred Hutchinson Cancer Research Center

This module provides the logic for the folder selection page of the IchorCurate app.
"""

# Import packages
import streamlit as st
import os

def display():
    st.title("Folder Selection")

    # Input field for folder path
    folder_path = st.text_input("Enter the path to the IchorCNA data you wish to curate. This should be a path to a folder containing subdirectories named for each sample")

    if folder_path:
        # Validate if the folder exists
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            st.session_state.selected_folder = folder_path
            st.success(f"Folder '{folder_path}' selected successfully!")
        else:
            st.error(f"The folder '{folder_path}' does not exist. Please try again.")
    else:
        st.warning("Please provide a valid folder path.")
    
    # Optinoally, allow users to specify an output directory for the curated solutions
    output_path = st.text_input("Optionally, specify an output directory for the curated solutions (default creates a new folder '/curated_solutions/') ")

    if output_path:
        st.session_state.output_path = output_path
        st.success(f"Output path '{output_path}' selected successfully!")
    else:
        st.warning("No output path specified. Default will be used.")
        st.session_state.output_path = "curated_solutions"

    #Once these are completed navigate to tracker dashboard
    if st.button("Continue to Solution Curation"):
        # Redirect to Tracker Dashboard
        #st.session_state.page = "Tracker Dashboard"
        st.rerun()  # Refresh app to redirect after login
        
