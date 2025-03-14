"""
projects_overview.py
v1.0.0, 3/14/2025
Branch: fredhutch-deployment
Author: Alexander Netzley, anetzley@fredhutch.org
Ha Lab, Fred Hutchinson Cancer Research Center

This module provides the logic for the projects overview page of the ichorCurate app.
"""

# Import packages
import streamlit as st
import yaml
import os

# Import user modules
from src.utils import load_config, count_samples, count_curated_samples, get_curating_users, get_latest_update, load_curated_solutions, format_filepath, generate_output_folders

def display():
    st.title("Projects Overview -- Deployed Version")
    config_path = os.path.join(st.session_state.backend, "config.yaml")

    config = load_config(config_path)

    # Table headers
    cols = st.columns([2, 2, 2, 1, 1, 1, 1, 1, 1])  # Adjust column width ratios
    with cols[0]:
        st.write("**Project Name**")
    with cols[1]:
        st.write("**Data Path**")
    with cols[2]:
        st.write("**Output Path**")
    with cols[3]:
        st.write("**# Samples**")
    with cols[4]:
        st.write("**# Curated Samples**")
    with cols[5]:
        st.write("**Curating Users**")
    with cols[6]:
        st.write("**Latest Update**")
    with cols[7]:
        st.write("**Edit Project**")
    with cols[8]:
        st.write("**Delete Project**")

    # Display a row for each project
    for project_name, project_info in config["projects"].items():
        #Instantiate a separate session state for each project and load in the existing solutions from the summary
        if project_name not in st.session_state:
            st.session_state[project_name] = {}
            load_curated_solutions(st.session_state.backend, project_name)

        data_path = project_info["data_path"]
        summary_path = project_info["summary_path"]
        output_path = project_info["output_path"]
        
        # Create a new row for the project
        cols = st.columns([2, 2, 2, 1, 1, 1, 1, 1, 1]) 

        # Column 1: Project Button
        with cols[0]:
            if st.button(project_name, key=f"project_{project_name}"):
                st.session_state.selected_project = project_name
                st.session_state.selected_folder = data_path
                st.session_state.output_path = output_path
                st.rerun()

        # Column 2: Data Path
        with cols[1]:
            st.write(f"`{data_path}`")

        # Column 3: Output Path
        with cols[2]:
            st.write(f"`{output_path}`")

        # Column 4: Number of Samples
        with cols[3]:
            st.write(count_samples(data_path))

        # Column 5: Number of Curated Samples
        with cols[4]:
            st.write(count_curated_samples(summary_path))

        # Column 6: Number of Curated Samples
        with cols[5]:
            st.write(get_curating_users(summary_path))

        # Column 7: Latest Update
        with cols[6]:
            st.write(get_latest_update(summary_path))
        
        # Column 8: Edit Project Button
        with cols[7]:
            if st.button("Edit Project", key=f"edit_{project_name}"):
                st.session_state.edit_project = project_name
                st.session_state.edit_data_path = data_path
                st.session_state.edit_output_path = output_path
                st.rerun()

        # Column 9: Delete Project Button
        with cols[8]:
            if st.button("Delete Project", key=f"delete_{project_name}", help="Delete this project"):
                st.session_state["delete_confirm"] = project_name  # Store project for confirmation modal
                st.rerun()

        # Show edit project form if edit is triggered
        if "edit_project" in st.session_state and st.session_state["edit_project"] == project_name:
            st.info(f"Editing project **{project_name}**")

            new_project_name = st.text_input("New Project Name", value=st.session_state["edit_project"])
            new_data_path = format_filepath(st.text_input("New Data Path", value=st.session_state["edit_data_path"]))
            new_output_path = format_filepath(st.text_input("New Output Path", value=st.session_state["edit_output_path"]))

            col1, col2 = st.columns(2)
            with col1:
                if st.button("❌ Cancel", key=f"cancel_edit_{project_name}"):
                    del st.session_state["edit_project"]
                    del st.session_state["edit_data_path"]
                    del st.session_state["edit_output_path"]
                    st.rerun()

            with col2:
                if st.button("💾 Save", key=f"save_edit_{project_name}"):
                    # Update config
                    if new_project_name != project_name:
                        #Move summary file
                        summary_path = os.path.join(st.session_state.backend, new_project_name, "curation_summary.txt")
                        generate_output_folders(st.session_state.backend, new_project_name)
                        os.rename(os.path.join(st.session_state.backend, project_name, "curation_summary.txt"), summary_path)
                        del config["projects"][project_name]
                    config["projects"][new_project_name] = {"data_path": new_data_path, "summary_path": summary_path, "output_path": new_output_path}

                    # Save updated YAML file
                    with open(config_path, "w") as file:
                        yaml.dump(config, file, default_flow_style=False)

                    del st.session_state["edit_project"]
                    del st.session_state["edit_data_path"]
                    del st.session_state["edit_output_path"]
                    st.success(f"Project '{project_name}' updated successfully!")
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
        new_data_path = format_filepath(st.text_input("Data Path"))
        new_output_path = format_filepath(st.text_input("Output Path"))

        if st.button("Add Project"):
            if new_project_name and new_data_path:
                new_summary_path = os.path.join(st.session_state.backend, new_project_name, "curation_summary.txt")

                # Update config
                config["projects"][new_project_name] = {"data_path": new_data_path, "summary_path": new_summary_path, "output_path": new_output_path}

                # Save to YAML
                with open(config_path, "w") as file:
                    yaml.dump(config, file, default_flow_style=False)

                st.success(f"Project '{new_project_name}' added!")
                st.rerun()
            else:
                st.error("Please enter a project name and correct data and output path.")