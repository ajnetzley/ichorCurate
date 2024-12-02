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

# Import user modules
from src.utils import export

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
    cols = st.columns([3, 2, 2, 2])  # Adjust column width ratios
    with cols[0]:
        st.write("**Sample**")
    with cols[1]:
        st.write("**Curated Solution**")
    with cols[2]:
        st.write("**User**")
    with cols[3]:
        st.write("**Export**")

    #Display a button for each sample folder, navigate to curation page when clicked
    for sample in sample_folders:
        
        # Check if the sample has a curated solution
        curated_solution = (
            st.session_state.curated_solutions[sample]
            if "curated_solutions" in st.session_state and sample in st.session_state.curated_solutions
            else None
        )

        #Extract the users and curated solutions, if curation has been performed
        if curated_solution:
            users = list(st.session_state.curated_solutions[sample].keys())
            solutions = list((st.session_state.curated_solutions[sample].values()))
            num_curations = len(users)
        else:
            num_curations = 0

        # Display the sample, curated solution, user, and export button for curated solutions
        if curated_solution:
            for i in range(num_curations):
                # Create a row
                cols = st.columns([3, 2, 2, 2])

                # Column 1: Sample Button
                with cols[0]:
                    if i == 0:
                        if st.button(sample, key=f"sample_{sample}_{users[i]}"):
                            # Store selected sample in session state and navigate to Curation Page
                            st.session_state.selected_sample = sample
                            st.session_state.page = "Curation"  # Trigger automatic navigation
                            st.rerun()  # Refresh the app to load the curation page
                        else:
                            st.write("")

                # Column 2: Curated Solution
                with cols[1]:
                    # Display a green letters and solution name
                    st.success(f"Selected: {solutions[i][-11:-4]}")

                # Column 3: User
                with cols[2]:
                    # Display a green letters and solution name
                    st.success(f"Curated by: {users[i]}")

                # Column 4: Export Button
                with cols[3]: 
                    if st.button(f"Export {sample}", key=f"export_{sample}_{users[i]}"):
                        st.write(f"Exported solution for {solutions[i][-11:-4]} for {sample}")

                        export(sample, solutions[i][-11:-4], base_sample_directory)
                        
        else:
            # Create a row
            cols = st.columns([3, 2, 2, 2])

            # Column 1: Sample Button
            with cols[0]:
                if st.button(sample, key=f"sample_{sample}"):
                    # Store selected sample in session state and navigate to Curation Page
                    st.session_state.selected_sample = sample
                    st.session_state.page = "Curation"
                    st.rerun()  # Refresh the app to load the curation page

        # Add a divider to separate rows
        st.divider()
