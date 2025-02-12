"""
login.py
v1.0.0, 2/12/2025
Branch: fredhutch-deployment
Author: Alexander Netzley, anetzley@fredhutch.org
Ha Lab, Fred Hutchinson Cancer Research Center

This module provides the logic for the folder selection page of the ichorCurate app.
"""

# Import packages
import streamlit as st
import os

def display():
    st.title("Folder Selection")
    
    # Optionally, allow users to specify an output directory for the curated solutions
    st.subheader("Output Data Filepath")
    output_path = st.text_input("Specify an output directory to save the curated solutions and curation summary")

    if output_path:
        # Add a leading and trailing "/" if not present
        if output_path[-1] != "/":
            output_path += "/"
        if output_path[0] != "/":
            output_path = "/" + output_path
        
        # Instantiate the output path for exporting files
        os.makedirs(output_path, exist_ok=True) 
        
        # Validate the folder was successfully made
        if os.path.exists(output_path) and os.path.isdir(output_path):
                st.session_state.output_path = output_path
                st.success(f"Folder '{output_path}' selected successfully!")

        else:
            st.error(f"The folder '{output_path}' does not exist. Please enter a new folder path.")
    else:
        st.warning("Please provide a valid folder path.")

    #Once these are completed navigate to tracker dashboard
    if "output_path" in st.session_state and st.session_state["output_path"] is not None:
        st.rerun()  # Refresh app to redirect after login
        