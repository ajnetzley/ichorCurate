"""
curation.py
v1.0.0, 11/6/2024
Author: Alexander Netzley, anetzley@fredhutch.org
Ha Lab, Fred Hutchinson Cancer Research Center

This module provides the main logic for the curation page of the IchorCurate app.
"""

# Import packages
import streamlit as st
import os
from streamlit_shortcuts import button, add_keyboard_shortcuts

# Import user modules
from src.utils import *

def display():
    """
    Main wrapper for the curation page display.
    """

    # Extract the sample name that was chosen to navigate here
    if "selected_sample" not in st.session_state:
        st.write("No sample selected, return to Tracker Dashboard and select a sample to curate.")
    
    else:
        ############################
        ### LOADING IN THE FILES ###
        ############################
        sample_name = st.session_state.selected_sample

        # Specify the directory containing the genome-wdie PDFs
        genome_wide_directory = os.path.join("test_data/", sample_name, sample_name)
        
        # Load the PDFs containing "genomeWide_n" and ending with ".pdf"
        genome_wide_pdf_files = [
            f for f in os.listdir(genome_wide_directory)
            if "genomeWide_n" in f and f.endswith(".pdf")
        ]

        # Loop through the directory and load and store the PDFs names of the per-chromosome plots
        for solution, _, files in os.walk(genome_wide_directory):
            # Extract the chromosome files
            chromosome_pdf_files = sorted([
                f for f in files
                if "CNA_chrchr" in f and f.endswith(".pdf")
            ], key=extract_chromosome_number)

            if chromosome_pdf_files:
                continue #Since all the chromosome plots have the same file name, we only need to find one solution to create the list

        # State for tracking which PDF is currently displayed
        if "pdf_index" not in st.session_state:
            st.session_state.pdf_index = 0
        if "solution_pdf" not in st.session_state:
            st.session_state.solution_pdf = None

        #########################################
        ### Potential Solutions - Genome-Wide ###
        #########################################

        # # Navigation Controls Column
        # with col_nav:
        st.subheader(f"Potential Solutions for Sample: {sample_name}")

        # Display navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if button("Previous", "ArrowLeft", None, hint=True) and st.session_state.pdf_index > 0:
                st.session_state.pdf_index -= 1

        with col2:
            if button("Next", "ArrowRight", None, hint=True) and st.session_state.pdf_index < len(genome_wide_pdf_files) - 1:
                st.session_state.pdf_index += 1

        # Display the current PDF as an image
        if genome_wide_pdf_files:
            current_pdf = genome_wide_pdf_files[st.session_state.pdf_index]
            st.session_state.current_pdf = current_pdf
            file_path = os.path.join(genome_wide_directory, current_pdf)
            pdf_image = get_pdf_first_page_image(file_path)

            #st.subheader(f"Displaying {current_pdf}")
            st.image(pdf_image, use_container_width=True)

            st.write(f"Showing Potential Solution {st.session_state.pdf_index + 1} of {len(genome_wide_pdf_files)}")

            # Button to set the current PDF as the solution
            with col3:
                if button("Set as Selected Solution", "Enter", None, hint=True):
                    st.session_state.solution_pdf = current_pdf
        else:
            st.write("No Genome-Wide PDF files found.")

        ############################################
        ### Potential Solutions - Per-Chromosome ###
        ############################################
        # Display checkboxes for each chromosome, and allow selecting
        selected_chromosomes, solution_folder_name = select_chromosomes("current", st.session_state.current_pdf, genome_wide_directory, genome_wide_pdf_files, chromosome_pdf_files)

        # Display selected PDFs in horizontal layout
        if selected_chromosomes:
            display_chromosome_plots(selected_chromosomes, genome_wide_directory, solution_folder_name, sample_name)

        ########################################
        ### Selected Solutions - Genome-Wide ###
        ########################################
        # with col_sol:
        st.subheader("Selected Solution")
        if st.session_state.solution_pdf:
            solution_path = os.path.join(genome_wide_directory, st.session_state.solution_pdf)
            solution_image = get_pdf_first_page_image(solution_path)
            #st.write(f"Solution PDF: {st.session_state.solution_pdf}")
            st.image(solution_image, use_container_width=True)
            
        else:
            st.write("No solution selected.")

        ###########################################
        ### Selected Solutions - Per-Chromosome ###
        ###########################################
        if st.session_state.solution_pdf:
            # Display checkboxes for each chromosome, and allow selecting
            selected_chromosomes, solution_folder_name = select_chromosomes("selected", st.session_state.solution_pdf, genome_wide_directory, genome_wide_pdf_files, chromosome_pdf_files)

            # Display selected PDFs in horizontal layout
            if selected_chromosomes:
                display_chromosome_plots(selected_chromosomes, genome_wide_directory, solution_folder_name, sample_name)

        ###################################
        ### Selected Solutions - Curate ###
        ###################################
        # Write selected solution, and return to dashboard page
        if button("Select as Curated Solution", "Ctrl+Enter", None, hint=True):

            # Save the selected solution in session state
            # st.session_state.curated_solution = {
            #     "sample": sample_name,
            #     "solution": st.session_state.solution_pdf,te
            # }
            st.session_state.curated_solutions[sample_name] = st.session_state.solution_pdf

            st.session_state.page = "Tracker Dashboard" # Navigate back to the tracker dashboard
            st.rerun()  # Refresh the app to load the tracker dashboard page
        