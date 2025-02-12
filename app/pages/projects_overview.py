"""
projects_overview.py
v0.3.0, 2/5/2025
Author: Alexander Netzley, anetzley@fredhutch.org
Ha Lab, Fred Hutchinson Cancer Research Center

This module provides the logic for the projects overview page of the ichorCurate app.
"""

# Import packages
import streamlit as st
import yaml
import os

# Import user modules
from src.utils import load_config, count_samples, count_curated_samples, get_curating_users, get_latest_update, load_curated_solutions

def display():
    st.title("Projects Overview")
    config_path = os.path.join(st.session_state.backend, "config.yaml")

    config = load_config(config_path)

    # Table headers
    cols = st.columns([2, 2, 1, 1, 2, 2, 1])  # Adjust column width ratios
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
    with cols[6]:
        st.write("**Delete Project**")

    # Display a row for each project
    for project_name, project_info in config["projects"].items():
        #Instantiate a separate session state for each project and load in the existing solutions from the metadata
        if project_name not in st.session_state:
            st.session_state[project_name] = {}
            load_curated_solutions(st.session_state.backend, project_name)

        data_path = project_info["data_path"]
        metadata_path = project_info["metadata_path"]
        
        # Create a new row for the project
        cols = st.columns([2, 2, 1, 1, 2, 2, 1]) 

        # Column 1: Project Button
        with cols[0]:
            if st.button(project_name, key=f"project_{project_name}"):
                st.session_state.selected_project = project_name
                st.session_state.selected_folder = data_path
                #st.session_state.output_path = "curated_solutions"
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

        # Column 7: Delete Project Button
        with cols[6]:
            if st.button("Delete Project", key=f"delete_{project_name}", help="Delete this project"):
                st.session_state["delete_confirm"] = project_name  # Store project for confirmation modal
                st.rerun()

        # Show confirmation message if delete is triggered
        if "delete_confirm" in st.session_state and st.session_state["delete_confirm"] == project_name:
            st.warning(f"Are you sure you want to delete project **{project_name}**? This will delete all associated curation metadata.")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("❌ Cancel", key=f"cancel_{project_name}"):
                    del st.session_state["delete_confirm"]
                    st.rerun()

            with col2:
                if st.button("🗑️ Confirm Delete", key=f"confirm_delete_{project_name}"):
                    # Remove project from config
                    del config["projects"][project_name]

                    # Save updated YAML file
                    with open(config_path, "w") as file:
                        yaml.dump(config, file, default_flow_style=False)

                    del st.session_state["delete_confirm"]
                    st.success(f"Project '{project_name}' deleted successfully!")
                    st.rerun()

        # Add a divider between projects
        st.divider()

     # Form to create a new project
    with st.expander("➕ Create New Project"):
        new_project_name = st.text_input("Project Name")
        new_data_path = st.text_input("Data Path")

        if st.button("Add Project"):
            # Ensure data_path ends with a "/"
            if not new_data_path.endswith("/"):
                new_data_path += "/"

            if new_project_name and new_data_path:
                new_metadata_path = os.path.join(st.session_state.backend, new_project_name, "curation_summary.txt")

                # Update config
                config["projects"][new_project_name] = {"data_path": new_data_path, "metadata_path": new_metadata_path}

                # Save to YAML
                with open(config_path, "w") as file:
                    yaml.dump(config, file, default_flow_style=False)

                st.success(f"Project '{new_project_name}' added!")
                st.rerun()
            else:
                st.error("Please enter both a project name and data path.")