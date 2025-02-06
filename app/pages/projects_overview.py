"""
projects_overview.py
v0.3.0, 2/5/2025
Author: Alexander Netzley, anetzley@fredhutch.org
Ha Lab, Fred Hutchinson Cancer Research Center

This module provides the logic for the projects overview page of the ichorCurate app.
"""

# Import packages
import streamlit as st
import os
import yaml
import json
import math

# Function to load the YAML config file
def load_config(config_path="/fh/fast/ha_g/user/anetzley/ichorCurate-backend/config.yaml"):
    with open(config_path, "r") as file:
        return yaml.safe_load(file)
    
# Function to count the number of samples (example: count files in data_path)
def count_samples(data_path):
    return str(math.floor(len(os.listdir(data_path))/4)) if os.path.exists(data_path) else 0

# Function to count curated samples (assumes curated samples are stored in metadata)
def count_curated_samples(metadata_path):
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, "r") as meta_file:
                metadata = json.load(meta_file)
            return len(metadata.get("curated_samples", []))  # Adjust based on your metadata structure
        except Exception as e:
            st.error(f"Could not load metadata: {e}")
            return str(0)
    return str(0)

# Load the config at the start of the app
config = load_config()

def display():
    st.title("Projects Overview")

    config = load_config()

    # Table headers
    cols = st.columns([2, 2, 1, 1, 2, 2])  # Adjust column width ratios
    with cols[0]:
        st.write("**Project Name**")
    with cols[1]:
        st.write("**Data Path**")
    with cols[2]:
        st.write("**# Samples**")
    with cols[3]:
        st.write("**# Curated Samples**")
    with cols[4]:
        st.write("**Curating Users**")
    with cols[5]:
        st.write("**Latest Update**")

    # Display a row for each project
    for project_name, project_info in config["projects"].items():
        data_path = project_info["data_path"]
        metadata_path = project_info["metadata_path"]
        
        num_samples = count_samples(data_path)
        num_curated_samples = count_curated_samples(metadata_path)

        # Create a new row for the project
        cols = st.columns([2, 2, 1, 1, 2, 2]) 

        # Column 1: Project Button
        with cols[0]:
            if st.button(project_name, key=f"project_{project_name}"):
                st.session_state.selected_project = project_name
                st.session_state.selected_folder = data_path
                st.session_state.output_path = "curated_solutions"
                st.rerun()

        # Column 2: Data Path
        with cols[1]:
            st.write(f"`{data_path}`")

        # Column 3: Number of Samples
        with cols[2]:
            st.write(num_samples)

        # Column 4: Number of Curated Samples
        with cols[3]:
            st.write(num_curated_samples)

        # Add a divider between projects
        st.divider()