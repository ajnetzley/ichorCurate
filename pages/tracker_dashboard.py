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
    base_sample_directory = "test_data/"

    #TODO update to just read folder names
    #TODO incorporate some way to upload a folder?

    sample_folders = [
        f for f in os.listdir(base_sample_directory) 
        if os.path.isdir(os.path.join(base_sample_directory, f))
        ]
    
    # Placeholder for the table layout
    table = []


    #Display a button for each sample folder, navigate to curation page when clicked
    for sample in sample_folders:
        curated_solution = None
        
        # Check if the sample has a curated solution
        if "curated_solutions" in st.session_state and sample in st.session_state.curated_solutions:
            curated_solution = st.session_state.curated_solutions[sample]


        # Create a row
        row = {}
        
        # Column 1: Sample Button
        button_clicked = st.button(sample)
        if button_clicked:
            # Store selected sample in session state and navigate to Curation Page
            st.session_state.selected_sample = sample
            st.session_state.page = "Curation"  # Trigger automatic navigation
            st.rerun()  # Refresh the app to load the curation page

        row['Sample'] = button_clicked

        # Column 2: Curated Solution
        if curated_solution:
            # Display a green letters and solution name
            # row['Curated Solution'] = st.markdown(f"""
            #     <style>
            #     .curated-button {{
            #         background-color: #28a745 !important; /* Green */
            #         color: white !important;            /* White text */
            #         border: 1px solid #e0e0e0;
            #         padding: 0.25rem 0.75rem;
            #         border-radius: 0.25rem;
            #         font-size: 18px;
            #         text-align: center;
            #         display: inline-block;
            #         cursor: not-allowed;
            #         width: 50%; /* Ensures consistency with Streamlit buttons */
            #         box-sizing: border-box; /* Ensure padding doesn't affect width */
            #     }}
            #     </style>
            #     <div class="curated-button">
            #         Selected: {curated_solution[-11:-4]}
            #     </div>
            # """, unsafe_allow_html=True)
            row['Curated Solution'] = f"Selected: {curated_solution[-11:-4]}"
        else:
            row['Curated Solution'] = None
        
        # Column 3: Export Button
        if curated_solution:
            export_button = st.button(f"Export {sample}", key=f"export_{sample}")
            row['Export'] = export_button
            if export_button:
                st.write(f"Exporting solution for {sample}...")  # Placeholder for export functionality
        else:
            row['Export'] = None

        table.append(row)

    # Now display the table-like layout using columns
    for row in table:
        cols = st.columns([3, 3, 3])
        with cols[0]:
            if row['Sample']:
                st.write("Sample Selected")
        with cols[1]:
            st.write(row['Curated Solution'])
        with cols[2]:
            if row['Export']:
                st.write("Export Button Clicked")