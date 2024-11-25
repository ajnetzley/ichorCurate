"""
utils.py
v1.0.0, 11/6/2024
Author: Alexander Netzley, anetzley@fredhutch.org
Ha Lab, Fred Hutchinson Cancer Research Center

This module provides helper functions for the IchorCurate app.
"""
# Import packages
import fitz  # PyMuPDF
import plotly.express as px
from PIL import Image
import re
import streamlit as st
import os

# Function to get the first page as an image from a PDF
def get_pdf_first_page_image(pdf_path):
    with fitz.open(pdf_path) as pdf:
        # Render the first page as an image
        first_page = pdf[0]
        pix = first_page.get_pixmap()  
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return img

# Function to obtain the matching folder name that contains a substring
def get_matching_folder(genome_wide_directory, extracted_solution_name):
    solution_details_folder = None
    for solution in os.listdir(genome_wide_directory):
        if os.path.isdir(os.path.join(genome_wide_directory, solution)) and extracted_solution_name in solution:
            solution_details_folder = solution
            break

    return solution_details_folder

# Function to extract chromosome number from filename
def extract_chromosome_number(file_name):
    # Regex to match either a number (1–22) or the letter "X" or "Y" before ".pdf"
    match = re.search(r'(1[0-9]|2[0-2]|\d|X|Y)\.pdf$', file_name, re.IGNORECASE)
    
    if match:
        chromosome = match.group(1)
        # Return integers for chromosomes 1–22, and specific values for X and Y to keep them sorted at the end
        if chromosome.isdigit():
            return int(chromosome)
        elif chromosome.upper() == 'X':
            return 23  # Place X after 22
        elif chromosome.upper() == 'Y':
            return 24  # Place Y after X #TODO Check if this is relevant
    return float('inf')  # Default to 'inf' if no match is found to push unrecognized items to the end

# Function to display and allow selecting of chromosomes
def select_chromosomes(display_mode, solution_pdf, genome_wide_directory, genome_wide_pdf_files, chromosome_pdf_files):
    
    # Chromosome-specific PDF selection)
    cols = st.columns(23)

    # Display checkboxes across the columns
    extracted_solution_name = re.search(r'n([^n]*?)\.pdf$', solution_pdf).group(1).replace('-', '_') # REGEX to extract the current solution name
    solution_details_folder = get_matching_folder(genome_wide_directory, extracted_solution_name)     

    selected_chromosomes = []
    for i, pdf_file in enumerate(chromosome_pdf_files):
        chrom_number = extract_chromosome_number(pdf_file)  # Extract chromosome number from filename
        if chrom_number == 23:
            chrom_number = "X"
        elif chrom_number == 24:
            chrom_number = "Y"
        checkbox_label = f"{chrom_number}"
        with cols[i % 23]:  # Distribute checkboxes across columns
            if st.checkbox(checkbox_label, key = display_mode + pdf_file):
                selected_chromosomes.append(pdf_file) #If the checkbox is selected, add the chromosome to the list of selected chromosomes

    return selected_chromosomes, solution_details_folder



# Function to plot the per-chromosome copy number data
def display_chromosome_plots(selected_chromosomes, genome_wide_directory, solution_details_folder, sample_name):
    # If just one chromosome is selected, take up the whole page
    if len(selected_chromosomes) == 1:
        pdf_path = os.path.join(genome_wide_directory, solution_details_folder, sample_name, selected_chromosomes[0])
        if os.path.exists(pdf_path):
            chrom_pdf_image = get_pdf_first_page_image(pdf_path)
            st.image(chrom_pdf_image, caption=f"Chromosome {extract_chromosome_number(selected_chromosomes[0])}", use_container_width=True)

    # If multiple chromosomes are selected, display them in a horizontal layout
    else:
        display_cols = st.columns(len(selected_chromosomes))  # Create one column per selected PDF

        for col, pdf_file in zip(display_cols, selected_chromosomes):
            pdf_path = os.path.join(genome_wide_directory, solution_details_folder, sample_name, pdf_file)
            if os.path.exists(pdf_path):
                chrom_pdf_image = get_pdf_first_page_image(pdf_path)
                col.image(chrom_pdf_image)#, caption=f"Chromosome {extract_chromosome_number(pdf_file)[0]}", use_container_width=True)    
            else:
                st.write(f"Chromosome {extract_chromosome_number(pdf_file)} PDF not found.")


