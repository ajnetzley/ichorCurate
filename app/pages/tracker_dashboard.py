"""
tracker_dashboard.py
v0.2.0, 1/15/2025
Author: Alexander Netzley, anetzley@fredhutch.org
Ha Lab, Fred Hutchinson Cancer Research Center

This module provides the main logic for the tracker dashboard page of the ichorCurate app.
"""

# Import packages
import streamlit as st
import os
import re

# Import user modules
from src.utils import get_tfx_and_ploidy, populate_summary, generate_summary_file, export, export_all

def display():
    st.subheader("Tracker Dashboard")

    # Create a button for each sample in the data directory
    sample_directory = st.session_state.selected_folder#"test_data/" 

    sample_folders = sorted([
        f for f in os.listdir(sample_directory) 
        if os.path.isdir(os.path.join(sample_directory, f))
        ])

    # Instantiate the output path for exporting files
    os.makedirs(st.session_state.output_path, exist_ok=True) 

    #Generate the summary
    summary = populate_summary(sample_folders, sample_directory, st.session_state.curated_solutions)

    # Buttons for exporting curation summary and all curations
    if st.button("Export Curation Summary"):
        generate_summary_file(summary, st.session_state.output_path)
        st.write(f"Summary file generated at {os.path.join(st.session_state.output_path, 'curation_summary.txt')}")

    if st.button("Export All Samples"):
        export_all(sample_folders, st.session_state.curated_solutions, sample_directory, st.session_state.output_path)
        st.write(f"All solutions exported to {st.session_state.output_path}")

    if st.button("Export All Curated Samples"):
        export_all(sample_folders, st.session_state.curated_solutions, sample_directory, st.session_state.output_path, curated_only=True)
        st.write(f"All curated solutions exported to {st.session_state.output_path}")

    # Table headers
    cols = st.columns([2, 2, 2, 2])  # Adjust column width ratios
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
                cols = st.columns([2, 2, 2, 2])

                #Extract and format the solution name from the pdf file name
                match = re.search(r"n([\d.]+)-p(\d+)\.pdf$", solutions[i])
                #formatted_solution_name = f"Normal {match.group(1)}, Ploidy {match.group(2)}"
                tumor_fraction, ploidy = get_tfx_and_ploidy(sample, sample_directory, match)
                formatted_solution_name = f"Tumor Fraction {tumor_fraction}, Ploidy {ploidy}"

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
                    st.success(f"Selected: {formatted_solution_name}")

                # Column 3: User
                with cols[2]:
                    # Display a green letters and solution name
                    st.success(f"Curated by: {users[i]}")

                # Column 4: Export Button
                with cols[3]: 
                    if st.button(f"Export Curated Solution ({formatted_solution_name})", key=f"export_{sample}_{users[i]}"):
                        st.write(f"Exported Curated Solution ({formatted_solution_name}) for {sample}")

                        export(sample, sample_directory, st.session_state.output_path, solutions[i][-11:-4])#TODO fix to remove sample
                
        else:
            # Create a row
            cols = st.columns([2, 2, 2, 2])

            # Column 1: Sample Button
            with cols[0]:
                if st.button(sample, key=f"sample_{sample}"):
                    # Store selected sample in session state and navigate to Curation Page
                    st.session_state.selected_sample = sample
                    st.session_state.page = "Curation"
                    st.rerun()  # Refresh the app to load the curation page
            
            # Column 4: Export Button for default export
            with cols[3]: 
                if st.button(f"Export Default Solution", key=f"export_{sample}"):
                    st.write(f"Exported default solution for {sample}")

                    export(sample, sample_directory, st.session_state.output_path)
            
        # Add a divider to separate rows
        st.divider()
    
