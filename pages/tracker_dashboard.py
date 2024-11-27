"""
tracker_dashboard.py
v0.1.0, 11/6/2024
Author: Alexander Netzley, anetzley@fredhutch.org
Ha Lab, Fred Hutchinson Cancer Research Center

This module provides the main logic for the tracker dashboard page of the IchorCurate app.
"""

# Import packages
import streamlit as st
import os
import re

def display():
    st.subheader("Tracker Dashboard")

    # Create a button for each sample in the data directory
    base_sample_directory = "test_data/"

    #TODO update to just read folder names
    #TODO incorporate some way to upload a folder?

    sample_folders = [
        f for f in os.listdir(base_sample_directory) 
        if os.path.isdir(os.path.join(base_sample_directory, f))
        ]

    # Table headers
    cols = st.columns([3, 3, 2])  # Adjust column width ratios
    with cols[0]:
        st.write("**Sample**")
    with cols[1]:
        st.write("**Curated Solution**")
    with cols[2]:
        st.write("**Export**")

    #Display a button for each sample folder, navigate to curation page when clicked
    for sample in sample_folders:
        
        # Check if the sample has a curated solution
        curated_solution = (
            st.session_state.curated_solutions[sample]
            if "curated_solutions" in st.session_state and sample in st.session_state.curated_solutions
            else None
        )

        # Create a row
        cols = st.columns([3, 3, 2])

        # Column 1: Sample Button
        with cols[0]:
            if st.button(sample, key=f"sample_{sample}"):
                # Store selected sample in session state and navigate to Curation Page
                st.session_state.selected_sample = sample
                st.session_state.page = "Curation"  # Trigger automatic navigation
                st.rerun()  # Refresh the app to load the curation page

        # Column 2: Curated Solution
        with cols[1]:
            if curated_solution:
                # Display a green letters and solution name
                st.success(f"Selected: {curated_solution[-11:-4]}")
            else:
                st.write("No solution curated yet")

        # Column 3: Export Button
        with cols[2]:
            if curated_solution:
                if st.button(f"Export {sample}", key=f"export_{sample}"):
                    st.write(f"Exporting solution for {sample}...")  # Placeholder for export functionality
            else:
                st.write("")  # Placeholder for empty cell
