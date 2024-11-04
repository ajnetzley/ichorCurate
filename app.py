import streamlit as st
import fitz  # PyMuPDF
import plotly.express as px
import pandas as pd
import os
from PIL import Image
from streamlit_shortcuts import button, add_keyboard_shortcuts
import re

# Setting page formats
st.set_page_config(layout="wide")

# Title of the app
st.title('IchorCurate')

################################
### LOADING IN THE PDF FILES ###
################################
# Specify the directory containing your PDFs
pdf_directory = "../IchorCNA/521R02_B01_CFFv2_ND0814_S2/"

# Load the PDFs containing "genomeWide_n" and ending with ".pdf"
genome_wide_pdf_files = [
    f for f in os.listdir(pdf_directory)
    if "genomeWide_n" in f and f.endswith(".pdf")
]

# Load the PDFs containing the per-chromosome plots
chromosome_pdf_files = sorted([
    f for f in os.listdir(pdf_directory)
    if "CNA_chrchr" in f and f.endswith(".pdf")
])

# State for tracking which PDF is currently displayed
if "pdf_index" not in st.session_state:
    st.session_state.pdf_index = 0
if "solution_pdf" not in st.session_state:
    st.session_state.solution_pdf = None

# Function to get the first page as an image from a PDF
def get_pdf_first_page_image(pdf_path):
    with fitz.open(pdf_path) as pdf:
        # Render the first page as an image
        first_page = pdf[0]
        pix = first_page.get_pixmap()  
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return img

# Function to extract chromosome number from filename
def extract_chromosome_number(file_name):
    match = re.search(r'(\d+)\.pdf$', file_name)
    return int(match.group(1)) if match else float('inf')  # Default to 'inf' if no number is found



##################
### APP LAYOUT ###
##################
# col_sol, col_nav = st.columns(2)


#########################################
### Potential Solutions - Genome-Wide ###
#########################################

# # Navigation Controls Column
# with col_nav:
st.subheader("Potential Solutions")
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
    st.image(pdf_image, use_column_width=True)

    st.write(f"Showing Potential Solution {st.session_state.pdf_index + 1} of {len(genome_wide_pdf_files)}")

    # Button to set the current PDF as the solution
    with col3:
        if button("Set as Solution", "Enter", None, hint=True):
            st.session_state.solution_pdf = current_pdf
else:
    st.write("No PDF files found matching the pattern.")

############################################
### Potential Solutions - Per-Chromosome ###
############################################
# Chromosome-specific PDF selection
st.subheader("View Chromosome PDFs")
cols = st.columns(11)

# Display checkboxes across the columns
selected_chromosomes = []
for i, pdf_file in enumerate(chromosome_pdf_files):
    chrom_number = extract_chromosome_number(pdf_file)  # Extract chromosome number from filename
    checkbox_label = f"{chrom_number}"
    with cols[i % 11]:  # Distribute checkboxes across columns
        if st.checkbox(checkbox_label):
            selected_chromosomes.append(pdf_file)


# Display each selected chromosome PDF
# Display selected PDFs
for pdf_file in selected_chromosomes:
    pdf_path = os.path.join(pdf_directory, pdf_file)
    if os.path.exists(pdf_path):
        chrom_pdf_image = get_pdf_first_page_image(pdf_path)
        st.image(chrom_pdf_image, caption=f"Chromosome {extract_chromosome_number(pdf_file)}", use_column_width=True)
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
    st.image(solution_image, use_column_width=True)
    
else:
    st.write("No solution selected.")


