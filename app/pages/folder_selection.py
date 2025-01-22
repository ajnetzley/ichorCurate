"""
login.py
v0.2.0, 1/15/2025
Author: Alexander Netzley, anetzley@fredhutch.org
Ha Lab, Fred Hutchinson Cancer Research Center

This module provides the logic for the folder selection page of the ichorCurate app.
"""

# Import packages
import streamlit as st
import os

def display():

    st.title("Folder Selection")

    # Input field for folder path
    st.subheader("Input Data Filepath")
    folder_path = st.text_input("Enter the path to the ichorCNA data you wish to curate. This should be a path to a folder containing only the data, consisting of subdirectories named for each sample")

    if folder_path:
        # Validate if the folder exists
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # Add a trailing "/" if not present
            if folder_path[-1] != "/":
                folder_path += "/"
            st.session_state.selected_folder = folder_path
            st.success(f"Folder '{folder_path}' selected successfully!")
        else:
            st.error(f"The folder '{folder_path}' does not exist. Please try again.")
    else:
        st.warning("Please provide a valid folder path.")
    
    # Optionally, allow users to specify an output directory for the curated solutions
    st.subheader("Output Data Filepath")
    st.write("Specify a directory to save the curated solutions, either select the default or input a custom path.")
    if st.button("Use default output path '/curated_solutions/'"):
        st.session_state.output_path = "curated_solutions"
        st.success(f"Output path '/curated_solutions/' selected successfully!")
        
    output_path = st.text_input("Specify a custom output directory for the curated solutions")

    if output_path:
        st.session_state.output_path = output_path
        st.success(f"Output path '{output_path}' selected successfully!")

    #Once these are completed navigate to tracker dashboard
    if st.button("Continue to Solution Curation") and "selected_folder" in st.session_state and "output_path" in st.session_state:
        st.session_state.folders_selected = True
        st.rerun()  # Refresh app to redirect after login
        
