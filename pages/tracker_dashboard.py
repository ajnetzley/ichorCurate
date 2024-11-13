"""
curation.py
v1.0.0, 11/6/2024
Author: Alexander Netzley, anetzley@fredhutch.org
Ha Lab, Fred Hutchinson Cancer Research Center

This module provides a the main logic for the curation page of the IchorCurate app.
"""

# Import packages
import streamlit as st
import os
import re

def display():
    st.subheader("Tracker Dashboard")

    # Create a button for each sample in the data directory
    base_sample_directory = "../IchorCNA/"

    # Matching pattern (subfolders that start with a number), #TODO adjust as necessary to accomodate sample folder names
    sample_folder_pattern = re.compile(r'^\d+')

    sample_folders = [
        f for f in os.listdir(base_sample_directory) 
        if os.path.isdir(os.path.join(base_sample_directory, f)) and sample_folder_pattern.match(f)
        ]

    #Display a button for each sample folder, navigate to curation page when clicked
    for sample in sample_folders:
        
        # Check if the sample has a curated solution
        if "curated_solution" in st.session_state and st.session_state.curated_solution["sample"] == sample:
            curated_solution = st.session_state.curated_solution["solution"]

            if st.button(f"Selected: {sample}", key=sample, help="Curated solution selected", disabled=True, use_container_width=True):
                pass  # Button is non-clickable since it's already curated
            st.write(f"Curated Solution: {curated_solution}")
    
        
        # Display a button for each sample folder that has NOT yet been curated
        else:
            if st.button(sample):
                # Store selected sample in session state and navigate to Curation Page
                st.session_state.selected_sample = sample
                st.session_state.page = "Curation"  # Trigger automatic navigation
                st.rerun()  # Refresh the app to load the curation page