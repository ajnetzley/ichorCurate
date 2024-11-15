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

    ################################
    ### LOADING IN THE PDF FILES ###
    ################################

    # Extract the sample name that was chosen to navigate here
    if "selected_sample" not in st.session_state:
        st.write("No sample selected, return to Tracker Dashboard and select a sample to curate.")
    
    else:
        sample_name = st.session_state.selected_sample

        # Specify the directory containing your PDFs
        pdf_directory = os.path.join("../IchorCNA/", sample_name)

        # Load the PDFs containing "genomeWide_n" and ending with ".pdf"
        genome_wide_pdf_files = [
            f for f in os.listdir(pdf_directory)
            if "genomeWide_n" in f and f.endswith(".pdf")
        ]

        # Load the PDFs containing the per-chromosome plots
        chromosome_pdf_files = sorted([
            f for f in os.listdir(pdf_directory)
            if "CNA_chrchr" in f and f.endswith(".pdf")
        ], key=extract_chromosome_number)


        # State for tracking which PDF is currently displayed
        if "pdf_index" not in st.session_state:
            st.session_state.pdf_index = 0
        if "solution_pdf" not in st.session_state:
            st.session_state.solution_pdf = None

        ##################
        ### APP LAYOUT ###
        ##################
        # col_sol, col_nav = st.columns(2)


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
            file_path = os.path.join(pdf_directory, current_pdf)
            pdf_image = get_pdf_first_page_image(file_path)

            #st.subheader(f"Displaying {current_pdf}")
            st.image(pdf_image, use_container_width=True)

            st.write(f"Showing Potential Solution {st.session_state.pdf_index + 1} of {len(genome_wide_pdf_files)}")

            # Button to set the current PDF as the solution
            with col3:
                if button("Set as Selected Solution", "Enter", None, hint=True):
                    st.session_state.solution_pdf = current_pdf
        else:
            st.write("No PDF files found matching the pattern.")

        ############################################
        ### Potential Solutions - Per-Chromosome ###
        ############################################
        # Chromosome-specific PDF selection)
        cols = st.columns(23)

        # Display checkboxes across the columns
        selected_chromosomes = []
        for i, pdf_file in enumerate(chromosome_pdf_files):
            chrom_number = extract_chromosome_number(pdf_file)  # Extract chromosome number from filename
            if chrom_number == 23:
                chrom_number = "X"
            elif chrom_number == 24:
                chrom_number = "Y"
            checkbox_label = f"{chrom_number}"
            with cols[i % 23]:  # Distribute checkboxes across columns
                if st.checkbox(checkbox_label):
                    selected_chromosomes.append(pdf_file)


        # Display selected PDFs in horizontal layout
        if selected_chromosomes:
            if len(selected_chromosomes) == 1:
                pdf_path = os.path.join(pdf_directory, selected_chromosomes[0])
                if os.path.exists(pdf_path):
                    chrom_pdf_image = get_pdf_first_page_image(pdf_path)
                    st.image(chrom_pdf_image, caption=f"Chromosome {extract_chromosome_number(selected_chromosomes[0])}", use_container_width=True)

            else:
                display_cols = st.columns(len(selected_chromosomes))  # Create one column per selected PDF

                for col, pdf_file in zip(display_cols, selected_chromosomes):
                    pdf_path = os.path.join(pdf_directory, pdf_file)
                    if os.path.exists(pdf_path):
                        chrom_pdf_image = get_pdf_first_page_image(pdf_path)
                        col.image(chrom_pdf_image)#, caption=f"Chromosome {extract_chromosome_number(pdf_file)[0]}", use_container_width=True)    
                    else:
                        st.write(f"Chromosome {extract_chromosome_number(pdf_file)} PDF not found.")

        ########################################
        ### Selected Solutions - Genome-Wide ###
        ########################################
        # with col_sol:
        st.subheader("Selected Solution")
        if st.session_state.solution_pdf:
            solution_path = os.path.join(pdf_directory, st.session_state.solution_pdf)
            solution_image = get_pdf_first_page_image(solution_path)
            #st.write(f"Solution PDF: {st.session_state.solution_pdf}")
            st.image(solution_image, use_container_width=True)
            
        else:
            st.write("No solution selected.")

        # Write selected solution, and return to dashboard page
        if button("Select as Curated Solution", "Ctrl+Enter", None, hint=True):

            # Save the selected solution in session state
            # st.session_state.curated_solution = {
            #     "sample": sample_name,
            #     "solution": st.session_state.solution_pdf,
            # }
            st.session_state.curated_solutions[sample_name] = st.session_state.solution_pdf

            st.session_state.page = "Tracker Dashboard" # Navigate back to the tracker dashboard
            st.rerun()  # Refresh the app to load the tracker dashboard page
        