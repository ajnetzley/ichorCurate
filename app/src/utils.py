"""
utils.py
v1.0.0, 2/12/2025
Branch: fredhutch-deployment
Author: Alexander Netzley, anetzley@fredhutch.org
Ha Lab, Fred Hutchinson Cancer Research Center

This module provides helper functions for the ichorCurate app.
"""
# Import packages
import fitz  # PyMuPDF
from PIL import Image
import re
import streamlit as st
import os
import shutil
import math
import datetime
import yaml
import stat

###########################
### project_overview.py ###
###########################
# Function to load the YAML config file
def load_config(config_path):
    with open(config_path, "r") as file:
        return yaml.safe_load(file)
    
# Function to count the number of samples (example: count files in data_path)
def count_samples(data_path):
    return str(math.floor(len(os.listdir(data_path))/4)) if os.path.exists(data_path) else 0

# Function to count curated samples (assumes curated samples are stored in metadata)
def count_curated_samples(summary_path):
    if os.path.exists(summary_path):
        with open(summary_path, "r") as file:
            lines = file.readlines()
        curated_samples = set() #only count unqiue samples

        for line in lines[1:]:
            parts = line.strip().split("\t")
            sample_name, curation_status, user, solution_filename = parts
            if curation_status != "None":
                curated_samples.add(sample_name)
        return str(len(curated_samples)) 
        
    return str(0)

# Function to extract the users who have curated samples
def get_curating_users(summary_path):
    if os.path.exists(summary_path):
        with open(summary_path, "r") as file:
            lines = file.readlines()
        users = set()

        for line in lines[1:]:
            parts = line.strip().split("\t")
            sample_name, curation_status, user, solution_filename = parts
            if curation_status != "None":
                users.add(user)
        return ", ".join(users)
        
    return ""

# Function to extract the time of the latest update
def get_latest_update(summary_path):
    if os.path.exists(summary_path):
        mod_time = os.path.getmtime(summary_path)
        return datetime.datetime.fromtimestamp(mod_time)
    else:
        return ""
    
# Function to load the curated solutions from the metadata file
def load_curated_solutions(directory, project):
    summary_file_path = os.path.join(directory, project, "curation_summary.txt")
    
    if os.path.exists(summary_file_path):
        with open(summary_file_path, 'r') as file:
            lines = file.readlines()[1:]  # Skip header

            for line in lines:
                parts = line.strip().split("\t")
                if len(parts) == 4 and parts[1] != "None":
                    sample, formatted_solution_name, user, curated_solution_filename = parts

                    # Read the existing summary into the session state
                    if "curated_solutions" not in st.session_state[project]:
                        st.session_state[project]["curated_solutions"] = {}

                    # Populate curated_solutions state with existing solutions
                    if sample not in st.session_state[project]["curated_solutions"]:
                        st.session_state[project]["curated_solutions"][sample] = {}

                    st.session_state[project]["curated_solutions"][sample][user] = curated_solution_filename


###################
### curation.py ###
###################

# Function to find the default solution and sort the genome wide pdfs so the optimal is listed first
def promote_default_pdf(genome_wide_directory, genome_wide_pdf_files):
        # Find the "optimal" subfolder and extract n and p values
        n_value, p_value = None, None
        for item in os.listdir(genome_wide_directory):
            if os.path.isdir(os.path.join(genome_wide_directory, item)) and "optimal" in item:
                # Extract n and p values using a regex
                match = re.search(r"n([\d.]+)_p(\d+)$", item)
                if match:
                    n_value, p_value = match.groups()
                    break

        # If an optimal subfolder is found, prioritize its PDF in the list
        if n_value and p_value:
            optimal_pdf = next(
                (f for f in genome_wide_pdf_files if f"n{n_value}-p{p_value}" in f), None
            )
            if optimal_pdf:
                # Reorder the list to have the optimal PDF first
                genome_wide_pdf_files.remove(optimal_pdf)
                genome_wide_pdf_files.insert(0, optimal_pdf)
        
        return genome_wide_pdf_files

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


############################
### tracker_dashboard.py ###
############################

# Function to extract and sort the sample folders from the filepath
def get_folders(directory):
    return sorted(
        (entry.name for entry in os.scandir(directory) if entry.is_dir())
    )
    
# Function to generate the output folder locations, prior to writing to them
def generate_output_folders(output_directory, project):
    # Create the output directory if it doesn't exist # TODO I feel like this won't work if the output path is relative vs gloabl, need to double check this
    os.makedirs(output_directory, exist_ok=True) # TODO update to a manual entry to specify output location

    # Create the output directory for this project
    os.makedirs(os.path.join(output_directory, project), exist_ok=True)

# Function to export the curated solution (UNNESTED VERSION)
def export(sample, base_sample_directory, output_directory, project, solution = "optimal"):
    #Overwrite existing solution if it exists
    if os.path.exists(os.path.join(output_directory, project, sample)):
        shutil.rmtree(os.path.join(output_directory, project, sample))
    os.makedirs(os.path.join(output_directory, project, sample), exist_ok=True)

    # Copy the curated solution to the output directory
    for root, dirs, files in os.walk(base_sample_directory + sample):

        #Copy over the genome-wide plot for the selected solution
        for file in files:

            # The "solution" input either contains the curated solution name, 
            # or the string "optimal". Here we check through all the files in 
            # the directory to find the one that matches the solution name
            if solution in file:
                shutil.copy(os.path.join(root, file), os.path.join(output_directory, project, sample))

                # Set permissions so copied files can be modified
                os.chmod(os.path.join(output_directory, project, sample, file), stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

        #Copy over the rest of the data for that solution
        for directory in dirs:
            if solution.replace("-", "_") in directory:
                shutil.copytree(os.path.join(root, directory), os.path.join(os.path.join(output_directory, project, sample), directory))

                # Set permissions for all files in the copied directory
                for dir_root, _, dir_files in os.walk(os.path.join(output_directory, project, sample, directory)):
                    for file in dir_files:
                        os.chmod(os.path.join(dir_root, file), stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

# # Function to export the curated solution (NESTED VERSION)
# def export(sample, base_sample_directory, output_directory, solution = "optimal"):
#     # Create the output directory if it doesn't exist # TODO I feel like this won't work if the output path is relative vs gloabl, need to double check this
#     os.makedirs(output_directory, exist_ok=True) # TODO update to a manual entry to specify output location

#     #Overwrite existing soltuion if it exists
#     if os.path.exists(os.path.join(output_directory, sample)):
#         shutil.rmtree(os.path.join(output_directory, sample))
#     os.makedirs(os.path.join(output_directory, sample), exist_ok=True)

#     # Copy the curated solution to the output directory
#     for root, dirs, files in os.walk(base_sample_directory + sample):

#         # Copy everything from the first layer
#         if root[len(base_sample_directory + sample):].count(os.sep) == 0:
#             for file in files:
#                 shutil.copy(os.path.join(root, file), os.path.join(output_directory, sample))

#         # For deeper layers, copy only the curated solution
#         elif root[len(base_sample_directory + sample):].count(os.sep) == 1:

#             #Copy over the genome-wide plot for the selected solution
#             for file in files:

#                 # The "solution" input either contains the curated solution name, 
#                 # or the string "optimal". Here we check through all the files in 
#                 # the directory to find the one that matches the solution name
#                 if solution in file:
#                     shutil.copy(os.path.join(root, file), os.path.join(output_directory, sample))

#             #Copy over the rest of the data for that solution
#             for directory in dirs:
#                 if solution.replace("-", "_") in directory:
#                     shutil.copytree(os.path.join(root, directory), os.path.join(os.path.join(output_directory, sample), directory))

# Function to get the tumor fraction and ploidy from the params file for a selected solution
def get_tfx_and_ploidy(sample, sample_directory, match):

    # Get the path to the params file
    sample_folder = os.path.join(sample_directory + sample)
    params_file_name = None

    for subfolder in os.listdir(sample_folder):
        #Select the folder of the solution that matches the selected solution
        if subfolder.endswith(f"n{match.group(1)}_p{match.group(2)}"):
            selected_solution_folder = os.path.join(sample_folder, subfolder)
            # Construct the expected params file name
            params_file_name = f"{sample}.params.txt"
            # Construct the path to params.txt
            potential_params_file = os.path.join(selected_solution_folder, params_file_name)
            if os.path.isfile(potential_params_file):
                params_file_path = potential_params_file
                break

    # Open the params files
    with open(params_file_path, "r") as file:
        lines = file.readlines()

    # Extract the tfx and ploidy
    tumor_fraction = lines[1].strip().split("\t")[1]
    ploidy = lines[1].strip().split("\t")[2]

    return tumor_fraction, ploidy

# Function to collect summary information
def populate_summary(sample_folders, sample_directory, curated_solutions):
    summary = []

    for sample in sample_folders:
        # Get curated solution from session state
        curated_solution = curated_solutions.get(sample, None)

        if curated_solution:
            users = list(curated_solution.keys())
            solutions = list(curated_solution.values())
            num_curations = len(users)

            for i in range(num_curations):
                match = re.search(r"n([\d.]+)-p(\d+)\.pdf$", solutions[i])
                tumor_fraction, ploidy = get_tfx_and_ploidy(sample, sample_directory, match)
                formatted_solution_name = f"Tumor Fraction {tumor_fraction}, Ploidy {ploidy}"
                summary.append(f"{sample}\t{formatted_solution_name}\t{users[i]}\t{solutions[i]}")
        else:
            summary.append(f"{sample}\tNone\tNone\tNone")

    return summary

# Function to generate a summary file of the curated solutions
def generate_summary_file(summary, output_directory, project):
    output_file_path = os.path.join(output_directory, project, "curation_summary.txt")
    with open(output_file_path, 'w') as file:
        file.write("Sample Name\tCuration Status\tUser\tSolution Filename\n")
        for line in summary:
            file.write(line + "\n")
    

# Function to export all samples
def export_all(sample_folders, curated_solutions, sample_directory, output_directory, project, curated_only=False):
    for sample in sample_folders:
        if sample in curated_solutions:
            for user, solution in curated_solutions[sample].items():
                export(sample, sample_directory, output_directory, project, solution[-11:-4])
        elif not curated_only:
            export(sample, sample_directory, output_directory, project)