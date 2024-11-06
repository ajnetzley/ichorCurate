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
            return 24  # Place Y after X
    return float('inf')  # Default to 'inf' if no match is found to push unrecognized items to the end
