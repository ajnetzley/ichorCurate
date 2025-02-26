"""
curation.py
v1.0.0, 2/12/2025
Branch: fredhutch-deployment
Author: Alexander Netzley, anetzley@fredhutch.org
Ha Lab, Fred Hutchinson Cancer Research Center

This module provides the main logic for the curation page of the ichorCurate app.
"""

# Import packages
import streamlit as st
import os
import datetime
from streamlit_shortcuts import button

# Import user modules
from src.utils import get_pdf_first_page_image, extract_chromosome_number, promote_default_pdf, select_chromosomes, display_chromosome_plots

def display():
    """
    Main wrapper for the curation page display.
    """
    # Extract project
    project = st.session_state.selected_project

    # Extract the sample name that was chosen to navigate here
    if "selected_sample" not in st.session_state[project]:
        st.write("No sample selected, return to Tracker Dashboard and select a sample to curate.")
    
    else:
        ############################
        ### LOADING IN THE FILES ###
        ############################
        sample_name = st.session_state[project]["selected_sample"]

        # Specify the directory containing the genome-wdie PDFs
        genome_wide_directory = os.path.join(st.session_state.selected_folder, sample_name)
        
        # Load the PDFs containing "genomeWide_n" and ending with ".pdf"
        genome_wide_pdf_files = sorted([
            f for f in os.listdir(genome_wide_directory)
            if "genomeWide_n" in f and f.endswith(".pdf")
        ])

        # Identify the default solution, and place this at the front of the list
        sorted_genome_wide_pdf_files = promote_default_pdf(genome_wide_directory, genome_wide_pdf_files)

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
        if sample_name not in st.session_state[project]["visualization"]:
            st.session_state[project]["visualization"][sample_name] = {}

        #Instantiate the visualization state for the current sample
        if "pdf_index" not in st.session_state[project]["visualization"][sample_name]:
            st.session_state[project]["visualization"][sample_name]["pdf_index"] = 0
        if "solution_pdf" not in st.session_state[project]["visualization"][sample_name]:
            st.session_state[project]["visualization"][sample_name]["solution_pdf"] = None
        if "current_pdf" not in st.session_state[project]["visualization"][sample_name]:
            st.session_state[project]["visualization"][sample_name]["current_pdf"] = None

        #########################################
        ### Potential Solutions - Genome-Wide ###
        #########################################

        # # Navigation Controls Column
        st.subheader(f"Potential Solutions for Sample: {sample_name}")

        # Toggle for enabling chromosome zoom
        chrom_zoom = False
        if st.toggle("Enable Chromosome Zoom"):
            chrom_zoom = True

        # Display navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if button("Previous", "ArrowLeft", None, hint=True) and st.session_state[project]["visualization"][sample_name]["pdf_index"] > 0:
                st.session_state[project]["visualization"][sample_name]["pdf_index"] -= 1

        with col2:
            if button("Next", "ArrowRight", None, hint=True) and st.session_state[project]["visualization"][sample_name]["pdf_index"] < len(sorted_genome_wide_pdf_files) - 1:
                st.session_state[project]["visualization"][sample_name]["pdf_index"] += 1

        # Display the current PDF as an image
        if sorted_genome_wide_pdf_files:
            current_pdf = sorted_genome_wide_pdf_files[st.session_state[project]["visualization"][sample_name]["pdf_index"]]
            st.session_state[project]["visualization"][sample_name]["current_pdf"] = current_pdf
            file_path = os.path.join(genome_wide_directory, current_pdf)
            pdf_image = get_pdf_first_page_image(file_path)

            #st.subheader(f"Displaying {current_pdf}")
            if st.session_state[project]["visualization"][sample_name]["pdf_index"] == 0:
                st.subheader("Default Solution")
            st.image(pdf_image, use_container_width=True)
            page_index = st.session_state[project]["visualization"][sample_name]["pdf_index"] + 1
            st.write(f"Showing Potential Solution {page_index} of {len(sorted_genome_wide_pdf_files)}")

            # Button to set the current PDF as the solution
            with col3:
                if button("Set as Selected Solution", "Enter", None, hint=True):
                    st.session_state[project]["visualization"][sample_name]["solution_pdf"] = current_pdf
        else:
            st.write("No Genome-Wide PDF files found.")

        ############################################
        ### Potential Solutions - Per-Chromosome ###
        ############################################
        if chrom_zoom:
            # Display checkboxes for each chromosome, and allow selecting
            selected_chromosomes, solution_folder_name = select_chromosomes("current", st.session_state[project]["visualization"][sample_name]["current_pdf"], genome_wide_directory, sorted_genome_wide_pdf_files, chromosome_pdf_files)

            # Display selected PDFs in horizontal layout
            if selected_chromosomes:
                display_chromosome_plots(selected_chromosomes, genome_wide_directory, solution_folder_name, sample_name)
        
        
        ###################################
        ### Reference Curated Solutions ###
        ###################################
        if st.toggle("Reference Curated Solution"):
            if not st.session_state[project]["curated_solutions"]:
                st.write(f"No curated solutions found.")
            else:
                st.subheader("Reference Curated Solution")

                curated_list = [f"{curated_sample}, {username}" for curated_sample, user_list in st.session_state[project]["curated_solutions"].items() for username in user_list]
                options = st.multiselect("Select Reference Curated Solution", curated_list, label_visibility="collapsed")

                for reference_sample in options:
                    reference_sample, username = reference_sample.split(", ")
                    solution_path = os.path.join(st.session_state.selected_folder, reference_sample, st.session_state[project]["curated_solutions"][reference_sample][username]["solution_pdf"])
                    solution_image = get_pdf_first_page_image(solution_path)
                    st.image(solution_image, use_container_width=True)

        ##########################
        ### Selected Solutions ###
        ##########################
        st.subheader("Selected Solution")

        # Display the selected solution PDF if selection has occured
        if st.session_state[project]["visualization"][sample_name]["solution_pdf"]:

            ########################################
            ### Selected Solutions - Genome-Wide ###
            ########################################
            solution_path = os.path.join(genome_wide_directory, st.session_state[project]["visualization"][sample_name]["solution_pdf"])
            solution_image = get_pdf_first_page_image(solution_path)
            #st.write(f"Solution PDF: {st.session_state.solution_pdf}")
            st.image(solution_image, use_container_width=True)
            
            ###########################################
            ### Selected Solutions - Per-Chromosome ###
            ###########################################
            if chrom_zoom:
                # Display checkboxes for each chromosome, and allow selecting
                selected_chromosomes, solution_folder_name = select_chromosomes("selected", st.session_state[project]["visualization"][sample_name]["solution_pdf"], genome_wide_directory, sorted_genome_wide_pdf_files, chromosome_pdf_files)

                # Display selected PDFs in horizontal layout
                if selected_chromosomes:
                    display_chromosome_plots(selected_chromosomes, genome_wide_directory, solution_folder_name, sample_name)

            ###################################
            ### Selected Solutions - Curate ###
            ###################################
            # Write selected solution, and return to dashboard page
            if button("Select as Curated Solution", "Ctrl+Enter", None, hint=True):

                # Intiialize the sample in the curated solutions dict if it has not already been curated
                if sample_name not in st.session_state[project]["curated_solutions"]:
                    st.session_state[project]["curated_solutions"][sample_name] = {}

                # Intialize the user profile in session state if it doesn't exist
                if st.session_state.username not in st.session_state[project]["curated_solutions"][sample_name]:
                    st.session_state[project]["curated_solutions"][sample_name][st.session_state.username] = {}

                # Save the selected solution in session state
                st.session_state[project]["curated_solutions"][sample_name][st.session_state.username] = {
                    "solution_pdf": st.session_state[project]["visualization"][sample_name]["solution_pdf"],
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

                st.session_state.page = "Tracker Dashboard" # Navigate back to the tracker dashboard
                st.rerun()  # Refresh the app to load the tracker dashboard page

        else:
            st.write("No solution selected.")