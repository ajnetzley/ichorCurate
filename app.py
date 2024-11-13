"""
app.py
v1.0.0, 11/6/2024
Author: Alexander Netzley, anetzley@fredhutch.org
Ha Lab, Fred Hutchinson Cancer Research Center

This module provides the wrapper function for running the IchorCurate app.
"""

# Import packages
import streamlit as st

# Import user modules
from pages.curation import display as curation_display
from pages.tracker_dashboard import display as tracker_dashboard_display
from src.utils import *

# Setting page formats
st.set_page_config(layout="wide")

# Title of the app
st.title('IchorCurate')

# Initialize page in session state if it doesn't exist
if "page" not in st.session_state:
    st.session_state.page = "Tracker Dashboard"

# Sidebar navigation with automatic selection
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Menu", ["Tracker Dashboard", "Curation"], index=0 if st.session_state.page == "Tracker Dashboard" else 1)

# Check and update the current page
if page != st.session_state.page:
    st.session_state.page = page  # Sync sidebar selection with session state

# Display the page
if st.session_state.page == "Tracker Dashboard":
    tracker_dashboard_display()
elif st.session_state.page == "Curation":
    curation_display()