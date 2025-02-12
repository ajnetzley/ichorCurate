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

    # # Input field for folder path
    # st.subheader("Input Data Filepath")
    # folder_path = st.text_input("Enter the path to the ichorCNA data you wish to curate. This should be a path to a folder containing only the data, consisting of subdirectories named for each sample")

    # if folder_path:
    #     # Validate if the folder exists
    #     if os.path.exists(folder_path) and os.path.isdir(folder_path):
    #         # Add a trailing "/" if not present
    #         if folder_path[-1] != "/":
    #             folder_path += "/"
    #         st.session_state.selected_folder = folder_path
    #         st.success(f"Folder '{folder_path}' selected successfully!")
    #     else:
    #         st.error(f"The folder '{folder_path}' does not exist. Please try again.")
    # else:
    #     st.warning("Please provide a valid folder path.")
    
    # Optionally, allow users to specify an output directory for the curated solutions
    st.subheader("Output Data Filepath")
    output_path = st.text_input("Specify an output directory to save the curated solutions and curation summary")

    if output_path:
        # Add a leading and trailing "/" if not present
        if output_path[-1] != "/":
            output_path += "/"
        if output_path[0] != "/":
            output_path = "/" + output_path
            
        # Validate if the folder exists
        if os.path.exists(output_path) and os.path.isdir(output_path):
                st.session_state.output_path = output_path
                st.success(f"Folder '{output_path}' selected successfully!")
        else:
            st.error(f"The folder '{output_path}' does not exist. Please enter a new folder path.")
    else:
        st.warning("Please provide a valid folder path.")

    #Once these are completed navigate to tracker dashboard
    if "output_path" in st.session_state:
        st.rerun()  # Refresh app to redirect after login
        