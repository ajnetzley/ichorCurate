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

# Import user modules
from src.utils import load_config, count_samples, count_curated_samples, get_curating_users, get_latest_update, load_curated_solutions

def display():
    st.title("Projects Overview")

    config = load_config(os.path.join(st.session_state.backend, "config.yaml"))

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
        #Instantiate a separate session state for each project and load in the existing solutions from the metadata
        if project_name not in st.session_state:
            st.session_state[project_name] = {}
            load_curated_solutions(st.session_state.backend, project_name)

        data_path = project_info["data_path"]
        metadata_path = project_info["metadata_path"]
        
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
            st.write(count_samples(data_path))

        # Column 4: Number of Curated Samples
        with cols[3]:
            st.write(count_curated_samples(metadata_path))

        # Column 5: Number of Curated Samples
        with cols[4]:
            st.write(get_curating_users(metadata_path))

        # Column 6: Latest Update
        with cols[5]:
            st.write(get_latest_update(metadata_path))

        # Add a divider between projects
        st.divider()