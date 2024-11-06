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

page = st.sidebar.selectbox("Menu:", ["Tracker Dashboard", "Curation"])

if page == "Tracker Dashboard":
    tracker_dashboard_display()
elif page == "Curation":
    curation_display()